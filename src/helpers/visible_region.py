from data_structures.definitions import Agent, Obstacle, PlayingRegion, grid_size
from helpers.collect_edges import collect_edges, collect_all_edges_and_vertices
from helpers.raycast import raycast
from helpers.asano_utils import cross, dist2, build_events, group_events
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

def visible_region_improved(p: Agent, obstacles: list[Obstacle], region: PlayingRegion):
    """
    Used only for the proposed approach.

    Sets for `p`, and returns, the visible region of `p` relative to `obstacles` and `region`.
    """

    edges, _ = collect_all_edges_and_vertices(obstacles, region)
    events = build_events(p, edges)
    grouped_events = group_events(events)

    active_edges: list[tuple[tuple[float, float], tuple[float, float]]] = []

    def intersect(edge: tuple[tuple[float, float], tuple[float, float]], theta: float) -> tuple[float, float]:
        px, py = p.x, p.y
        rx, ry = math.cos(theta), math.sin(theta)

        (ax, ay), (bx, by) = edge
        sx, sy = bx - ax, by - ay

        rxs = cross(rx, ry, sx, sy)
        if abs(rxs) < 1e-9:
            return None  # parallel or collinear

        apx, apy = ax - px, ay - py

        t = cross(apx, apy, sx, sy) / rxs
        u = cross(apx, apy, rx, ry) / rxs

        if t < 0:
            return None  # behind ray

        if u < -1e-9 or u > 1 + 1e-9:
            return None  # outside segment

        ix = px + t * rx
        iy = py + t * ry

        return (ix, iy)

    def nearest_intersection(theta: float):
        closest = None
        best_dist = float('inf')

        for e in active_edges:
            pt = intersect(e, theta)
            if pt is not None:
                d = dist2(p, pt)
                if d < best_dist:
                    best_dist = d
                    closest = pt

        return closest

    # --- initialize active edges at angle 0 ---
    for e in edges:
        if intersect(e, 0.0) is not None:
            active_edges.append(e)

    points = []

    for group in grouped_events:
        theta = group[0].angle

        prev_pt = nearest_intersection(theta - 1e-9)

        # --- remove all ending edges first ---
        for ev in group:
            for e in ev.end_edges:
                if e in active_edges:
                    active_edges.remove(e)

        # --- then add all starting edges ---
        for ev in group:
            for e in ev.start_edges:
                active_edges.append(e)

        next_pt = nearest_intersection(theta + 1e-9)

        if prev_pt:
            points.append(prev_pt)
        if next_pt:
            points.append(next_pt)

    poly = shapely.Polygon(points)

    p.visibility_region = shapely.set_precision(poly.simplify(grid_size, preserve_topology=True), grid_size)
    return p.visibility_region