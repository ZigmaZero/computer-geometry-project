from data_structures.definitions import Agent, Obstacle, PlayingRegion, grid_size
from helpers.collect_edges import collect_edges
from helpers.raycast import raycast
import math
import shapely

# returns a polygon representing the visible region of p
def visible_region(p: Agent, obstacles: list[Obstacle], region: PlayingRegion):
    """
    Used only for the baseline approach.

    Sets for `p`, and returns, the visible region of `p` relative to `obstacles` and `region`.
    """
    px, py = p.x, p.y

    angles = []
    edges = collect_edges(obstacles, region)
    for (x1, y1), (x2, y2) in edges:
        for vx, vy in [(x1, y1), (x2, y2)]:
            theta = math.atan2(vy - py, vx - px)
            angles.extend([theta - 1e-9, theta, theta + 1e-9])

    intersections = []

    for theta in angles:
        # cast ray, find minimum hit point, append to intersections
        ray = raycast(p.point, theta, region)

        closest_point = None
        min_dist = float("inf")

        for (x1, y1), (x2, y2) in edges:
            segment = shapely.LineString([(x1, y1), (x2, y2)])
            inter = ray.intersection(segment)

            if not inter.is_empty:
                if isinstance(inter, shapely.Point):
                    dist = inter.distance(p.point)
                    if dist < min_dist:
                        min_dist = dist
                        closest_point = inter

        if closest_point:
            intersections.append((theta, closest_point))

    # sort by angle
    intersections.sort(key=lambda x: x[0])

    # extract polygon
    points = [pt for _, pt in intersections]

    p.visibility_region = shapely.set_precision(shapely.Polygon([(pt.x, pt.y) for pt in points]).simplify(1e-6, preserve_topology=True), grid_size)
    return p.visibility_region