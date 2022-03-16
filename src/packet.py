
# Represents a network packet.
class Packet:
    def __init__(self, flow_id):
        """
        Per-flow metadata.
        """
        self.flow_id_ = flow_id
        self.arrival_clock_ = 0
        self.total_latency_ = 0
        self.queueing_delay_ = 0
        self.is_finalized_ = False

    def get_flow_id(self):
        return self.flow_id_

    def get_total_latency(self):
        return self.total_latency_

    def get_queueing_delay(self):
        return self.queueing_delay_

    def get_arrival_clock(self):
        return self.arrival_clock_

    def check_not_finalized(self):
        if self.is_finalized_:
            print("Cannot modify a finalized packet.")
        return not self.is_finalized_

    def add_latency(self, lat):
        if self.check_not_finalized:
            self.total_latency_ += lat

    # def increment_latency(self):
    #     self.add_latency(1.0)

    def set_queueing_delay(self, delay):
        if self.check_not_finalized():
            self.queueing_delay_ = delay

    def set_arrival_clock(self, clock):
        if self.check_not_finalized():
            self.arrival_clock_ = clock

    def finalize(self):
        if self.check_not_finalized():
            self.is_finalized_ = True

