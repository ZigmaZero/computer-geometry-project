from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
from data_structures.definitions import Agent, Obstacle, PlayingRegion, Faction
import shapely

def polygon_to_path(poly):
    vertices = []
    codes = []

    # --- exterior ---
    x, y = poly.exterior.coords.xy
    exterior = list(zip(x, y))

    vertices.extend(exterior)
    codes.extend([Path.MOVETO] + [Path.LINETO]*(len(exterior)-2) + [Path.CLOSEPOLY])

    # --- holes ---
    for interior in poly.interiors:
        x, y = interior.coords.xy
        ring = list(zip(x, y))

        vertices.extend(ring)
        codes.extend([Path.MOVETO] + [Path.LINETO]*(len(ring)-2) + [Path.CLOSEPOLY])

    return Path(vertices, codes)

def plot_visibility(agent: Agent, obstacles: list[Obstacle], region: PlayingRegion=None):
    """
    Plots the visible region of an agent on the playing region with obstacles.
    """
    fig, ax = plt.subplots()

    visibility_polygon = agent.visibility_region

    # --- Plot playing region (optional) ---
    if region is not None:
        x, y = region.polygon.exterior.xy
        ax.fill(x, y, alpha=0.05, edgecolor='black', linewidth=1, label="Region")

    # --- Plot obstacles ---
    for i, obs in enumerate(obstacles):
        poly = obs.polygon
        x, y = poly.exterior.xy
        ax.fill(x, y, alpha=0.6, edgecolor='black', linewidth=1)

    # --- Plot visibility polygon ---
    if visibility_polygon is not None:
        if isinstance(visibility_polygon, shapely.Polygon):
            polys = [visibility_polygon]
        elif isinstance(visibility_polygon, shapely.MultiPolygon):
            polys = list(visibility_polygon.geoms)
        else:
            polys = []

        for poly in polys:
            path = polygon_to_path(poly)
            patch = PathPatch(path, edgecolor='blue', alpha=0.3, linewidth=1)
            ax.add_patch(patch)

    # --- Plot agent ---
    ax.plot(agent.x, agent.y, 'ro', label="Agent")

    # --- Formatting ---
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, region.x if region else None)
    ax.set_ylim(0, region.y if region else None)

    ax.set_title("Visibility Visualization")
    ax.legend(loc="upper right")

    plt.show()

def plot_control(agentlist: list[Agent], obstacles: list[Obstacle], region: PlayingRegion):
    """
    Plots the control region of agents on the playing region with obstacles and other agents.
    """
    fig, ax = plt.subplots()

    if region is not None:
        x, y = region.polygon.exterior.xy
        ax.fill(x, y, alpha=0.05, edgecolor='black', linewidth=1)

    # --- Plot obstacles ---
    for obs in obstacles:
        x, y = obs.polygon.exterior.xy
        ax.fill(x, y, alpha=0.6, facecolor='black', edgecolor='black', linewidth=1)

    # --- Generate distinct colors per agent ---
    cmap = plt.get_cmap('tab10', len(agentlist))  # or 'tab20' if many agents

    # --- Plot control regions ---
    for i, agent in enumerate(agentlist):
        color = cmap(i)  # one fixed color per agent

        control_region = agent.control_region
        if control_region is not None:
            if isinstance(control_region, shapely.Polygon):
                polys = [control_region]
            elif isinstance(control_region, shapely.MultiPolygon):
                polys = list(control_region.geoms)
            else:
                polys = []

            for poly in polys:
                path = polygon_to_path(poly)
                patch = PathPatch(path, facecolor=color, edgecolor=color, alpha=0.3, linewidth=1)
                ax.add_patch(patch)

        # --- Plot agent ---
        ax.plot(agent.x, agent.y, 'o', color=color)

    # --- Formatting ---
    ax.set_aspect('equal', adjustable='box')
    if region:
        ax.set_xlim(0, region.x)
        ax.set_ylim(0, region.y)

    ax.set_title("Control Visualization")
    plt.show()

def plot_faction_control(factions: list[Faction], obstacles: list[Obstacle], region: PlayingRegion):
    """
    Plot control regions by faction with respect to obstacles and playing region
    """
    fig, ax = plt.subplots()

    if region is not None:
        x, y = region.polygon.exterior.xy
        ax.fill(x, y, alpha=0.05, edgecolor='black', linewidth=1)

    # --- Plot obstacles ---
    for obs in obstacles:
        x, y = obs.polygon.exterior.xy
        ax.fill(x, y, alpha=0.6, facecolor='black', edgecolor='black', linewidth=1)

    # --- Generate distinct colors per faction ---
    cmap = plt.get_cmap('tab10', len(factions))  # or 'tab20' if many agents

    # --- Plot control regions ---
    for i, faction in enumerate(factions):
        color = cmap(i)  # one fixed color per faction

        control_region = faction.control_region
        if control_region is not None:
            if isinstance(control_region, shapely.Polygon):
                polys = [control_region]
            elif isinstance(control_region, shapely.MultiPolygon):
                polys = list(control_region.geoms)
            else:
                polys = []

            for poly in polys:
                path = polygon_to_path(poly)
                patch = PathPatch(path, facecolor=color, edgecolor=color, alpha=0.3, linewidth=1)
                ax.add_patch(patch)

        # --- Plot agent ---
        for agent in faction.agentlist:
            ax.plot(agent.x, agent.y, 'o', color=color)

    # --- Formatting ---
    ax.set_aspect('equal', adjustable='box')
    if region:
        ax.set_xlim(0, region.x)
        ax.set_ylim(0, region.y)

    ax.set_title("Control Visualization")
    plt.show()