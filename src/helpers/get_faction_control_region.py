import shapely
from data_structures.definitions import Faction, grid_size

def get_faction_control_region(faction: Faction):
    faction.control_region = shapely.unary_union([shapely.set_precision(a.control_region.buffer(0), grid_size) for a in faction.agentlist])
    return faction.control_region