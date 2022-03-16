class FlowMetadata:
    def __init__(self):
        """
        Per-flow metadata.
        """
        self.num_windows = 0
        self.num_packets = 0
        self.last_packet_idx = 0
        self.queue_start_idx = 0
        self.cumulative_agg_delay = 0

    def record_flow_packet_arrival(self, idx, z):
        """
        :type idx: int
        :type z: int
        :rtype: int
        """
        # Time since start of queue
        tssq = idx - self.queue_start_idx

        # This packet corresponds to a new queue
        if self.num_packets == 0 or tssq >= z:
            self.num_windows += 1
            self.queue_start_idx = idx
            self.cumulative_agg_delay += z

        # Compute the AggregateDelay for the existing queue
        else:
            self.cumulative_agg_delay += (z - tssq)

        # Update the last idx and packet count
        self.last_packet_idx = idx
        self.num_packets += 1

        return self.cumulative_agg_delay

    def get_expected_payoff(self, clk):
        windowed_agg_delay = float(self.cumulative_agg_delay) / self.num_windows
        return windowed_agg_delay / (clk - self.last_packet_idx + 1)
