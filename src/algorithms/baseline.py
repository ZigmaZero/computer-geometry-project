from data_structures.definitions import *
from helpers.visible_region import visible_region
from helpers.control_region import control_region
from helpers.get_faction_control_region import get_faction_control_region

def baseline_algorithm(region: PlayingRegion, obs: list[Obstacle], agentlist: list[Agent], factions: list[Faction]):
    """
    Baseline algorithm for visibility-constrained faction control.

    Calculates each faction's control over the playing region and appends them to the object data.

    Returns the whole list of agents and factions, because that's easier to plot with.
    """

    for agent in agentlist:
        visible_region(agent, obs, region)

    for agent in agentlist:
        control_region(agent, agentlist, obs, region)

    for faction in factions:
        faction.control_region = get_faction_control_region(faction)

    return agentlist, factions