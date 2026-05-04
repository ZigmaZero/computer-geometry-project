from data_structures.definitions import Agent, PlayingRegion
import shapely
from shapely.ops import split

# helper to make a half plane
def make_distance_half_plane(p: Agent, q: Agent, region: PlayingRegion) -> shapely.Polygon:
    """
    Returns a polygon approximating the half-plane where
    `d(p, r) > d(q, r)`
    """
    px, py = p.x, p.y
    qx, qy = q.x, q.y

    # difference
    dx = qx - px
    dy = qy - py

    # perpendicular
    dx_ = dy
    dy_ = -dx

    # midpoint
    mx = (px + qx) / 2
    my = (py + qy) / 2

    # large number
    R = max(region.x, region.y) * 10

    # points of the half-plane
    bisector = shapely.LineString([
        (mx + dx_ * R, my + dy_ * R),
        (mx - dx_ * R, my - dy_ * R)
    ])

    split_polys = shapely.ops.split(region.polygon, bisector)

    # choose the one that does NOT contain p
    for geo in split_polys.geoms:
        if not geo.contains(p.point):
            return geo