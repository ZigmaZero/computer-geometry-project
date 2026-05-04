from data_structures.definitions import *
from algorithms.proposed import proposed_algorithm
from testing.inputs.input_generation import build_random_input
from visualization.plot_utils import plot_faction_control

# interactive constraints for generation~

region_x = 10
region_y = 10
obstacle_count = 4
obstacle_vertex_min = 3
obstacle_vertex_max = 3
faction_count = 2
agent_count = 2

interactiveTestInput = build_random_input(region_x, region_y, obstacle_count, obstacle_vertex_min, obstacle_vertex_max, faction_count, agent_count)
proposed_algorithm(interactiveTestInput.region, interactiveTestInput.obstacles, interactiveTestInput.agentlist, interactiveTestInput.factions)
plot_faction_control(interactiveTestInput.factions, interactiveTestInput.obstacles, interactiveTestInput.region)