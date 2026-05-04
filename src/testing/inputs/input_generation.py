from data_structures.definitions import *
import time
from algorithms.baseline import baseline_algorithm
from algorithms.proposed import proposed_algorithm
from testing.inputs.generate_agents import sample_agents_in_region
from testing.inputs.generate_factions import assign_factions
from testing.inputs.generate_obstacles import generate_obstacles

class TestInput:
    def __init__(self, region: PlayingRegion, agentlist: list[Agent], obstacles: list[Obstacle], factions: list[Faction]):
        self.agentlist = agentlist
        self.obstacles = obstacles
        self.region = region
        self.factions = factions

    def run_test(self):
        start = time.perf_counter()
        proposed_algorithm(self.region, self.obstacles, self.agentlist, self.factions)
        end = time.perf_counter()
        proposed = end - start

        # reset agents and factions' computed regions
        for agent in self.agentlist:
            agent.visibility_region = None
            agent.control_region = None

        for faction in self.factions:
            faction.control_region = None

        start = time.perf_counter()
        baseline_algorithm(self.region, self.obstacles, self.agentlist, self.factions)
        end = time.perf_counter()
        baseline = end - start

        return baseline, proposed

def build_random_input(region_x: float = 10,
                       region_y: float = 10,
                       obstacle_count: int = 4,
                       obstacle_vertex_min: int = 3,
                       obstacle_vertex_max: int = 4,
                       faction_count: int = 2,
                       agent_count: int = 2) -> TestInput:
    if region_x < 1:
        region_x = 1
    if region_x > 1000000:
        region_x = 1000000
    if region_y < 1:
        region_y = 1
    if region_y > 1000000:
        region_y = 1000000
    if obstacle_count < 0:
        obstacle_count = 0
    if obstacle_count > 5000:
        obstacle_count = 5000
    if obstacle_vertex_min < 3:
        obstacle_vertex_min = 3
    if obstacle_vertex_max > 100:
        obstacle_vertex_max = 100
    if faction_count < 1:
        faction_count = 1
    if faction_count > 16:
        faction_count = 16
    if agent_count < faction_count:
        agent_count = faction_count
    if agent_count > 1000:
        agent_count = 1000

    region = PlayingRegion(region_x, region_y)

    obstacles = generate_obstacles(
        obstacle_count, region, obstacle_vertex_min,
        obstacle_vertex_max)

    agentlist = sample_agents_in_region(region, obstacles, agent_count)

    factions = assign_factions(agentlist, faction_count)

    return TestInput(region, agentlist, obstacles, factions)