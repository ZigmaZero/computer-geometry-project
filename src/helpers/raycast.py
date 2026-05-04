from data_structures.definitions import PlayingRegion
import shapely
import math

def raycast(p: shapely.Point, angle: float, r: PlayingRegion):
    """
    Used only for the baseline approach.

    Casts a ray from `p` towards a far extent in the direction `angle`. 
    The endpoint of the ray is guaranteed to be beyond the playing region `r`.
    """
    radius = r.x + r.y
    far_point = shapely.Point(p.x + math.cos(angle) * radius, p.y + math.sin(angle) * radius)
    return shapely.LineString([(p.x, p.y), (far_point.x, far_point.y)])