import random
import numpy as np
import shapely
from data_structures.definitions import Obstacle, PlayingRegion, Agent

def sample_agents_in_region(region: PlayingRegion, obstacles: list[Obstacle], agent_count: int, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    agentlist = []

    # make region but with holes
    region_poly = region.polygon
    obstacle_polys = [o.polygon for o in obstacles]
    region_with_holes = region_poly.difference(shapely.unary_union(obstacle_polys))

    for _ in range(agent_count):
        while True:
            p = shapely.Point(random.uniform(0, region.x), random.uniform(0, region.y))

            # Check if it is inside the actual polygon
            if region_with_holes.contains(p):
                # ensure that the agent is not too close to other agents
                valid = True
                for a in agentlist:
                    if a.point.distance(p) < 0.001:
                        valid = False
                        break
                if valid:
                    agentlist.append(Agent(p.x, p.y))
                    break

    return agentlist