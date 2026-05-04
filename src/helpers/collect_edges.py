from data_structures.definitions import PlayingRegion, Obstacle

def collect_edges(obstacles: list[Obstacle], region: PlayingRegion) -> list[tuple[float, float]]:
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