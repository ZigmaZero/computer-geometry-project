from data_structures.definitions import Agent
from data_structures.event import Event
import math

def angle(p: Agent, v: tuple[float, float]):
    """
    Obtains the angle of v from p relative to the x-axis in radians.
    """
    px, py = p.x, p.y
    vx, vy = v[0], v[1]
    return math.atan2(vy - py, vx - px)

def dist2(p: Agent, v: tuple[float, float]):
    """
    Obtains the squared distance of line pv.
    """
    return (v[0] - p.x)**2 + (v[1] - p.y)**2

def normalize_angle(theta: float) -> float:
    if theta < 0:
        theta += 2 * math.pi
    return theta

def build_events(p: Agent, edges: list[tuple[tuple[float, float], tuple[float, float]]]):
    """
    Utility function for Asano's plane sweep algorithm.

    Builds a list of vertex events from the list of edges, providing the querying agent p.
    """
    vertex_map: dict[tuple[float, float], Event] = {}

    def get_event(v):
        if v not in vertex_map:
            theta = normalize_angle(angle(p, v))
            vertex_map[v] = Event(v, theta, dist2(p, v))
        return vertex_map[v]

    for a, b in edges:
        ev_a = get_event(a)
        ev_b = get_event(b)

        theta_a = ev_a.angle
        theta_b = ev_b.angle

        # Compute angular difference
        d = theta_b - theta_a
        if d <= -math.pi:
            d += 2 * math.pi
        elif d > math.pi:
            d -= 2 * math.pi

        # If d > 0: a -> b is CCW small arc
        if d > 0:
            ev_a.start_edges.append((a, b))
            ev_b.end_edges.append((a, b))
        else:
            ev_b.start_edges.append((a, b))
            ev_a.end_edges.append((a, b))

    # Return events sorted by angle, then distance
    events = list(vertex_map.values())
    events.sort(key=lambda e: (e.angle, e.dist2))

    return events

def group_events(events: list[Event], eps=1e-9):
    """
    Group events by their angle for batch processing.
    """
    groups = []
    events.sort(key=lambda e: e.angle)

    current = [events[0]]
    for e in events[1:]:
        if abs(e.angle - current[0].angle) < eps:
            current.append(e)
        else:
            groups.append(current)
            current = [e]
    groups.append(current)

    return groups

def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx