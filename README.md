# Visibility-Constrained Faction Control Problem

## Problem
Given the bounds of the playing region, the list of obstacles as simple polygons, 
and a number of agents separated into factions placed at separate points, 
we want to find the control region of each faction: that is, the set of points visible to 
one or more agents belonging to that faction, while not being closer to any agent from any other faction.

## Approach
- Baseline: Raycasting for the visible region as a visibility polygon, then clip by the union of "forbidden regions" with respect to other agents. Forbidden regions are derived by finding the intersection of the distance half-plane with respect to the other agent with that agent's visibility polygon. Faction control regions are computed from the union of its members' control regions.
- Proposed: Use Asano's plane sweep algorithm to find the visibility polygon, then iteratively clip by "forbidden regions" with respect to candidate agents. Candidates are obtained by early rejecting cases where that agent cannot possibly affect the control region. Faction control regions are computed from the union of its members' control regions.

## Constraints
- Region size: Within 1x1 to 1000x1000
- Obstacles: Up to 100 simple polygons. Polygons have up to 6 vertices.
- Faction count: 1-4
- Agent count: No. of factions to 40
- Acceptable error range: 0.001

## Results
- Speedup: Varied, but around 900% faster in normal usage.
- Dataset: Randomly generated according to constraints in test batches, see report for details.

## How to Run
pip install -r requirements.txt
python src/main.py
