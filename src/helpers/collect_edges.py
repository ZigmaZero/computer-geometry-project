from data_structures.definitions import PlayingRegion, Obstacle
import shapely

def collect_edges(obstacles: list[Obstacle], region: PlayingRegion) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """
    Used only for the baseline approach.
    
    Extracts edges from `obstacles` and `region` polygons.
    """
    edges = []

    # obstacles
    for obs in obstacles:
        coords = list(obs.polygon.exterior.coords)
        for i in range(len(coords) - 1):
            edges.append((coords[i], coords[i+1]))

    # playing region
    coords = list(region.polygon.exterior.coords)
    for i in range(len(coords) - 1):
        edges.append((coords[i], coords[i+1]))

    return edges

def collect_edges_and_vertices(poly: shapely.Polygon) -> tuple[list[tuple[tuple[float, float], tuple[float, float]]], list[tuple[float, float]]]:
    """
    Used only for the proposed approach.

    Extracts edges and vertices from a polygon `poly`.
    """
    coords = poly.exterior.coords
    vertices = [coords[i] for i in range(len(coords) - 1)]
    edges = [(coords[i], coords[i+1]) for i in range(len(coords) - 1)]

    return edges, vertices

def collect_all_edges_and_vertices(obstacles: list[Obstacle], region: PlayingRegion)  -> tuple[list[tuple[tuple[float, float], tuple[float, float]]], list[tuple[float, float]]]:
    """
    Used only for the proposed approach.
    
    Extracts edges and vertices from `obstacles` and `region` polygons.
    """
    polys = [region.polygon] + [obs.polygon for obs in obstacles]
    edges: list[tuple[tuple[float, float], tuple[float, float]]] = []
    vertices: list[tuple[float, float]] = []
    for poly in polys:
        e, v = collect_edges_and_vertices(poly)
        edges.extend(e)
        vertices.extend(v)

    return edges, vertices