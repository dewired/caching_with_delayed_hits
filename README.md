Assignment 2 - Advanced Computer Networks (CS 740)
=============

As a part of an Assignment, we were given a task to re-implement
a scaled-down version of networking system paper. This is a scaled-down working 
implementation of the paper [Caching with Delayed Hits](https://dl.acm.org/doi/10.1145/3387514.3405883).



## Replication and Usage
 Check out the code repository:

```
git clone https://github.com/dewired/caching_with_delayed_hits.git
```

To run:

```
python main.py
```
The values of the CAPACITY and Z can be changed in `main.py` to see the effects of different Z and capacities.

The output of this gives us the total latencies for both the caching policies in timesteps.
```
Total latency for LRU: 22609 timesteps.
Total latency for LRU-MAD: 20048 timesteps.
LRU with Minimum Aggregate Delay is faster than LRU by 11.32734751647574 %.
```
The authors of this work have provided an example (anonymized) trace file containing 5K requests is provided in the
`data/` directory, where each line of the trace has the following format: `timestamp;object_id`.
(Note: The `timestamp` field is ignored in the current implementation! At the moment, each line
of the trace represents one timestep; to encode zero request arrivals on timestep *x*, simply leave
the *x*'th line of the trace file empty.) More details about this work
 can be found [here](https://github.com/cmu-snap/Delayed-Hits).