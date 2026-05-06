from data_structures.definitions import *
from algorithms.proposed import proposed_algorithm
from testing.benchmark.test_bench import TestBench
from testing.inputs.input_generation import build_random_input
from visualization.plot_utils import plot_faction_control

# test_bench = TestBench(100, 100, 10, 3, 3, 2, 2)
# test_bench.bench()

# interactive constraints for generation~

region_x = 100
region_y = 100
obstacle_count = 20
obstacle_vertex_min = 3
obstacle_vertex_max = 5
faction_count = 4
agent_count = 10

interactiveTestInput = build_random_input(region_x, region_y, obstacle_count, obstacle_vertex_min, obstacle_vertex_max, faction_count, agent_count)
proposed_algorithm(interactiveTestInput.region, interactiveTestInput.obstacles, interactiveTestInput.agentlist, interactiveTestInput.factions)
plot_faction_control(interactiveTestInput.factions, interactiveTestInput.obstacles, interactiveTestInput.region)