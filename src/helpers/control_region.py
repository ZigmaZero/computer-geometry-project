from data_structures.definitions import Agent, Obstacle, PlayingRegion, grid_size
from helpers.visible_region import visible_region
from helpers.make_distance_half_plane import make_distance_half_plane
import shapely

def control_region(agent: Agent, agentlist: list[Agent], obstacles: list[Obstacle], region: PlayingRegion):
    """
    Used only for the baseline approach.

    Sets for `agent`, and returns, the control region for `agent` relative to the list of agents `agentlist`, the list of obstacles `obstacles`, and the playing region `region`.
    """
    # --- Step 1: ensure visibility ---
    if not agent.visibility_region:
        visible_region(agent, obstacles, region)

    control_poly = agent.visibility_region

    if control_poly.is_empty:
        agent.control_region = control_poly
        return control_poly

    fq_list = []

    for q in agentlist:
        if q == agent:
            continue

        # ensure visibility for q
        if not q.visibility_region:
            visible_region(q, obstacles, region)

        vis_q = q.visibility_region

        # --- Step 2: build half-plane polygon D_Q ---
        D_q = make_distance_half_plane(agent, q, region)

        # --- Step 3: F_Q = Vis(Q) ∩ D_Q ---
        F_q = vis_q.intersection(D_q)

        if not F_q.is_empty:
            fq_list.append(F_q)

    # --- Step 4: union + single subtraction ---
    if fq_list:
        F_union = shapely.unary_union(fq_list)
        control_poly = control_poly.difference(F_union)

        # clean geometry once
        control_poly = control_poly.buffer(0)

    agent.control_region = shapely.set_precision(control_poly, grid_size)
    return agent.control_region