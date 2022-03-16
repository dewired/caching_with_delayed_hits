# import DLinkedNodeedNode
from base_cache import BaseCache
from flow_metadata import FlowMetadata


class DLinkedNode:
    def __init__(self):
        self.key = 0
        self.value = 0
        self.prev = None
        self.next = None


class LruMadCache(BaseCache):
    def __init__(self, capacity, z):
        """
        :type capacity: int
        """
        super().__init__()
        self.size = 0
        self.capacity = capacity
        self.kCacheMissLatency = z
        self.records = {}  # Dict mapping flow IDs to records
        self.entries = {}  # Dict mapping flow IDs to CacheEntries

        self.head, self.tail = DLinkedNode(), DLinkedNode()

        self.head.next = self.tail
        self.tail.prev = self.head

    def record_packet_arrival(self, packet):
        key = packet.get_flow_id()
        if key in self.records:
            self.records[key].record_flow_packet_arrival(packet.get_arrival_clock(), self.kCacheMissLatency)
        else:
            flow_metadata = FlowMetadata()
            self.records[key] = flow_metadata
            self.records[key].record_flow_packet_arrival(packet.get_arrival_clock(), self.kCacheMissLatency)

    def _add_node(self, node):
        """
        Always add the new node right after head.
        """
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        node = self.cache.get(key, None)
        if not node:
            # go to memory -- add latency
            return -1

        # move the accessed node to the head;
        # self._move_to_head(node)
        return node.value

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        node = self.cache.get(key)

        if not node:
            new_node = DLinkedNode()
            new_node.key = key
            new_node.value = value

            self.cache[key] = new_node
            self._add_node(new_node)

            self.size += 1

            if self.size > self.capacity:
                # pop the tail
                # tail = self._pop_tail()
                # del self.cache[tail.key]
                # self.size -= 1

                min_cost = float('inf')
                flow_id_to_evict = ""
                for key in self.cache.keys():
                    candidate = key
                    candidate_cost = self.records[candidate].get_expected_payoff(self.clk)

                    if candidate_cost < min_cost:
                        min_cost = candidate_cost
                        flow_id_to_evict = candidate
                node_to_evict = self.cache.get(flow_id_to_evict, None)
                del self.cache[node_to_evict.key]
                self.size -= 1

        else:
            # update the value.
            node.value = value
