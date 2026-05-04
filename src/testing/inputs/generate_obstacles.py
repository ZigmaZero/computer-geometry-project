import random
import shapely
import numpy as np
from data_structures.definitions import Obstacle
from scipy.spatial import Voronoi

# --- Helper: Convert infinite Voronoi regions to finite polygons ---
def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions to finite regions.
    Source adapted from: https://stackoverflow.com/a/20678647
    """
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = np.ptp(vor.points).max() * 2

    # Map ridge vertices
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    for p1, region_idx in enumerate(vor.point_region):
        vertices = vor.regions[region_idx]

        if all(v >= 0 for v in vertices):
            new_regions.append(vertices)
            continue

        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue

            # Compute missing endpoint
            t = vor.points[p2] - vor.points[p1]
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_vertices.append(far_point.tolist())
            new_region.append(len(new_vertices) - 1)

        # Sort region vertices counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = [v for _, v in sorted(zip(angles, new_region))]

        new_regions.append(new_region)

    return new_regions, np.asarray(new_vertices)


# --- Helper: radial polygon inside a cell ---
def random_polygon_in_cell(cell: shapely.Polygon, v_min, v_max, shrink=0.8):
    """
    Generate a simple polygon inside a given shapely Polygon (cell)
    using radial sampling from centroid.
    """
    if cell.is_empty or not cell.is_valid:
        return None

    centroid = cell.centroid
    cx, cy = centroid.x, centroid.y

    n = random.randint(v_min, v_max)

    angles = np.sort(np.random.uniform(0, 2 * np.pi, n))
    points = []

    for theta in angles:
        dx, dy = np.cos(theta), np.sin(theta)

        # Ray from centroid
        far_point = shapely.Point(cx + dx * 1e5, cy + dy * 1e5)
        ray = shapely.Polygon([(cx, cy), (far_point.x, far_point.y), (far_point.x + 1e-6, far_point.y + 1e-6)])

        # Intersect ray with boundary
        line = cell.boundary.intersection(shapely.Point(cx, cy).buffer(1e5).boundary)

        # More robust: use a long segment
        from shapely.geometry import LineString
        ray_line = LineString([(cx, cy), (cx + dx * 1e5, cy + dy * 1e5)])
        inter = cell.boundary.intersection(ray_line)

        if inter.is_empty:
            continue

        # Extract farthest intersection point
        if "Point" in inter.geom_type:
            pts = [inter]
        else:
            pts = list(inter.geoms)

        dists = [(p.distance(centroid), p) for p in pts]
        _, boundary_pt = max(dists, key=lambda x: x[0])

        # Shrink inward
        px = cx + (boundary_pt.x - cx) * shrink
        py = cy + (boundary_pt.y - cy) * shrink
        points.append((px, py))

    if len(points) < 3:
        return None

    poly = shapely.Polygon(points)
    if not poly.is_valid:
        poly = poly.buffer(0)

    return poly if poly.is_valid else None


# --- Main function ---
def generate_large_M(
    M, x_max, y_max, v_min, v_max, seed=None
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Step 1: sample points
    points = np.column_stack((
        np.random.uniform(0, x_max, M),
        np.random.uniform(0, y_max, M)
    ))

    # Step 2: Voronoi
    vor = Voronoi(points)

    # Step 3: finite regions
    regions, vertices = voronoi_finite_polygons_2d(vor)

    bbox = shapely.box(0, 0, x_max, y_max)

    result = []

    for region in regions:
        poly_coords = vertices[region]
        cell = shapely.Polygon(poly_coords)

        # Step 4: clip to bounding box
        cell = cell.intersection(bbox)

        if cell.is_empty or not cell.is_valid:
            continue

        # Step 5: generate polygon inside cell
        poly = random_polygon_in_cell(cell, v_min, v_max)

        if poly is not None and bbox.contains(poly):
            result.append(poly)

    return result

def random_simple_polygon(n):
    angles = np.sort(np.random.uniform(0, 2*np.pi, n))
    radii = np.random.uniform(0.5, 1.0, n)

    points = [(r*np.cos(a), r*np.sin(a)) for r, a in zip(radii, angles)]
    return shapely.Polygon(points).buffer(0)


def generate_small_M(M, x_max, y_max, v_min, v_max, seed=None, max_attempts=1000):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    polys = []

    attempts = 0
    while len(polys) < M and attempts < max_attempts:
        attempts += 1

        n = random.randint(v_min, v_max)
        poly = random_simple_polygon(n)

        # scale to reasonable size
        sx = random.uniform(5, x_max / 2)
        sy = random.uniform(5, y_max / 2)
        poly = shapely.affinity.scale(poly, sx, sy)

        # translate into box
        tx = random.uniform(0, x_max)
        ty = random.uniform(0, y_max)
        poly = shapely.affinity.translate(poly, tx, ty)

        # clip to bounds (optional but safer)
        bbox = shapely.Polygon([(0,0),(x_max,0),(x_max,y_max),(0,y_max)])
        poly = poly.intersection(bbox)

        if poly.is_empty or not poly.is_valid:
            continue

        if type(poly) == shapely.geometry.multipolygon.MultiPolygon:
            poly = poly.geoms[0]

        if all(not poly.intersects(p) for p in polys):
            polys.append(poly)

    return polys

def generate_polygons(M, x_max, y_max, v_min, v_max, seed=None):
    if M < 4:
        return generate_small_M(M, x_max, y_max, v_min, v_max, seed=seed)
    else:
        return generate_large_M(
            M, x_max, y_max, v_min, v_max, seed=seed
        )

def generate_obstacles(M, region, vertex_min, vertex_max, seed=None):
    obstacles = []
    polys = generate_polygons(M, region.x, region.y, vertex_min, vertex_max, seed=seed)
    for poly in polys:
        coords = [coord for coord in poly.exterior.coords]
        obstacles.append(Obstacle(coords))
    return obstacles