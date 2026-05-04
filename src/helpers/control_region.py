from data_structures.definitions import Agent, Obstacle, PlayingRegion, grid_size
from helpers.visible_region import visible_region, visible_region_improved
from helpers.make_distance_half_plane import make_distance_half_plane
from helpers.bbox_intersects import bbox_intersects
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

def calculate_all_control_regions(agentlist: list[Agent], obstacles: list[Obstacle], region: PlayingRegion):
    """
    Used only for the proposed approach.

    Sets for all agents, but does NOT return, the control regions relative to `obstacles` and `region`.
    """
    for agent in agentlist:
        if not agent.visibility_region:
            visible_region_improved(agent, obstacles, region)

    tree = shapely.STRtree([q.visibility_region for q in agentlist])

    for agent in agentlist:
        control_poly = agent.visibility_region

        if control_poly.is_empty:
            agent.control_region = control_poly
            continue

        indices = tree.query(control_poly)

        for idx in indices:
            q = agentlist[idx]  # map back to agent

            if q is agent:
                continue

            vis_q = q.visibility_region

            if vis_q.is_empty:
                continue

            # bbox reject
            if not bbox_intersects(control_poly.bounds, vis_q.bounds):
                continue

            # build D_q late
            D_q = make_distance_half_plane(agent, q, region)

            if not bbox_intersects(control_poly.bounds, D_q.bounds):
                continue

            # now real intersection
            clip = vis_q.intersection(D_q)

            if clip.is_empty:
                continue

            control_poly = control_poly.difference(clip)

            if control_poly.is_empty:
                break

        agent.control_region = shapely.set_precision(control_poly, grid_size)