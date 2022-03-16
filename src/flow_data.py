
# Container for flow-related data.

class FlowData:
    def __init__(self):
        self.indices = []

    def get_indices(self):
        return self.indices

    # def get_idx_range(self):
    #     if self.indices:
    #         return 0
    #     else :
    #         return self.indices.back() - self.indices.front()

    def add_packet(self, idx):
        self.indices.append(idx)

# TODO: add trace logic
