from data_structures.definitions import PlayingRegion, Agent, Faction, Obstacle
from algorithms.baseline import baseline_algorithm
from algorithms.proposed import proposed_algorithm

region = PlayingRegion(10, 10)

agent1 = Agent(5,5)
agent2 = Agent(3,9)
agentlist = [agent1, agent2]

faction1 = Faction([agent1, agent2])
factions = [faction1]

obstacles = [
    Obstacle([(2,2), (4,2), (4,4), (2,4)]),
    Obstacle([(6,6), (8,6), (7,8)]),
    Obstacle([(6,4),(6.3,4),(6.3,4.3),(6,4.3)])
]

agentlist, factions = baseline_algorithm(region, obstacles, agentlist, factions)
agentlist, factions = proposed_algorithm(region, obstacles, agentlist, factions)