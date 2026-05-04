from data_structures.definitions import PlayingRegion, Obstacle, Agent, Faction
from helpers.visible_region import visible_region_improved
from helpers.control_region import calculate_all_control_regions
from helpers.get_faction_control_region import get_faction_control_region

def proposed_algorithm(region: PlayingRegion, obs: list[Obstacle], agentlist: list[Agent], factions: list[Faction]):
    """
    Proposed algorithm for visibility-constrained faction control.
    Calculates each faction's control over the playing region and appends them to the object data.
    Returns the whole list of agents and factions, because that's easier to plot with.
    """

    for agent in agentlist:
        visible_region_improved(agent, obs, region)

    calculate_all_control_regions(agentlist, obs, region)

    for faction in factions:
        faction.control_region = get_faction_control_region(faction)

    return agentlist, factions