class BaseCache:
    def __init__(self):
        self.clk = 0
        self.total_latency = 0
        self.memory_entries = set()
        self.completed_reads = {}
        self.packet_queues = {}
        self.kCacheMissLatency = 10
        self.cache = {}
        self.target_clk_to_flow_id = {}
        self.flow_id_to_target_clk = {}
        self.cache_hits = 0

    def get_clock(self):
        return self.clk

    def get_total_latency(self):
        return self.total_latency

    def get_z(self):
        return self.kCacheMissLatency

    def increment_clock(self):
        self.clk += 1

    def record_packet_arrival(self, packet):
        print("This method is overridden")

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        print("This method is overridden")

    # Handles any blocking read completions on this cycle.
    def process_all(self, processed_packets):
        if self.clk in self.target_clk_to_flow_id.keys():
            key = self.target_clk_to_flow_id[self.clk]
            packet_queue = self.packet_queues[key]

    #         // Commit the queued entries
            self.get(packet_queue[0].get_flow_id())
            processed_packets.extend(packet_queue)
    #       Purge the queue, as well as the bidict mapping
            packet_queue.clear()
            del self.packet_queues[key]
            del self.target_clk_to_flow_id[self.clk]
            del self.flow_id_to_target_clk[key]

    #   Finally, increment the clock
        self.increment_clock()

    # Processes the parameterized packet.
    def process_packet(self, packet, processed_packets):
        packet.set_arrival_clock(self.clk)
        key = packet.get_flow_id()

        # Record arrival of the packet at the cache and cache set
        self.record_packet_arrival(packet)
        # cache_set.recordPacketArrival(packet);

        if key not in self.memory_entries:
            # update memory
            self.memory_entries.add(key)
            # update cache
            self.put(key, key)
            # print("cache updated")

        # flow is cached -- process the packet immediately
        if key in self.cache.keys():
            # print("checking cache")

            packet.finalize()
            processed_packets.append(packet)
            self.total_latency += packet.get_total_latency()
            self.cache_hits += 1
        # else, either perform a a) blocking read from memory
        # b) wait for an existing blocking read to complete. Insert
        # this packet into the corresponding packet queue.
        else:
            if key not in self.packet_queues.keys():
                # If this flow's packet queue doesn't yet exist, this is the
                # blocking packet, and its read completes on cycle (clk + z).
                target_clock = self.clk + self.kCacheMissLatency - 1
                self.target_clk_to_flow_id[target_clock] = key
                self.flow_id_to_target_clk[key] = target_clock
                packet.add_latency(self.kCacheMissLatency)
                packet.finalize()
                # initialise a q for this flow
                self.packet_queues[key] = []
                self.packet_queues[key].append(packet)
            else:
                # update the flows packet queue
                target_clk = self.flow_id_to_target_clk.get(key)
                packet.set_queueing_delay(len(self.packet_queues[key]))
                packet.add_latency(target_clk - self.clk + 1)
                packet.finalize()
                self.packet_queues[key].append(packet)
            self.total_latency += packet.get_total_latency()
        # Process any completed reads
        self.process_all(processed_packets)

    def get(self, param):
        pass

