from lru_aggdelay_cache import LruMadCache
from lru_cache import LRUCache
from packet import Packet
from csv import reader

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    CAPACITY = 5
    Z = 10
    # Instantiating the two caches
    lru_cache = LRUCache(CAPACITY, Z)
    lru_mad_cache = LruMadCache(CAPACITY, Z)
    processed_packets = []
    # open file in read mode
    with open('../data/trace.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        # Iterate over each row in the trace file
        for row in csv_reader:
            # print(row[0].split(";")[1])
            key = row[0].split(";")[1]
            lru_cache.process_packet(Packet(key), processed_packets)
            lru_mad_cache.process_packet(Packet(key), processed_packets)

    print("Total latency for LRU:", lru_cache.total_latency, "timesteps.")
    print("Total latency for LRU-MAD:", lru_mad_cache.total_latency, "timesteps.")
    if lru_mad_cache.total_latency < lru_cache.total_latency:
        print("LRU with Minimum Aggregate Delay is faster than LRU by",
              (lru_cache.total_latency - lru_mad_cache.total_latency) * 100 / lru_cache.total_latency,
              "%. ")
    # print(lru_cache.cache_hits)
    # print(lru_mad_cache.cache_hits)
    # print(len(processed_packets))
