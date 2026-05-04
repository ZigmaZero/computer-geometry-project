import random
from data_structures.definitions import Agent, Faction

def distribute_shuffled(N, B, seed=None):
    if N == 1:
        return [list(range(N))]

    if N < B or N < 2 or B < 2:
        raise ValueError("Require N >= B >= 2")

    rng = random.Random(seed)  # optional reproducibility
    data = list(range(N))
    rng.shuffle(data)

    q, r = divmod(N, B)
    result = []
    start = 0

    for i in range(B):
        size = q + 1 if i < r else q
        result.append(data[start:start + size])
        start += size

    return result

def assign_factions(agentlist: list[Agent], faction_count: int, seed=None):
    buckets = distribute_shuffled(len(agentlist), faction_count, seed=seed)
    factions = []
    for bucket in buckets:
        factions.append(Faction([agentlist[i] for i in bucket]))
    return factions