import shapely

class PlayingRegion:
    def __init__(self, x: float, y: float):
        # the playing region's coordinates are from (0,0) to (x,y)
        self.x: float = x
        self.y: float = y
        self.polygon: shapely.Polygon = shapely.Polygon([(0,0), (x,0), (x,y), (0,y)])

class Agent:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.point: shapely.Point = shapely.Point(x, y)
        self.visibility_region: shapely.Polygon = None
        self.control_region: shapely.MultiPolygon = None

class Obstacle:
    def __init__(self, pointlist: list[tuple[float, float]]):
        self.pointlist: list[tuple[float, float]] = pointlist
        self.polygon: shapely.Polygon = shapely.Polygon(pointlist)

class Faction:
    def __init__(self, agentlist: list[Agent]):
        self.control_region: shapely.MultiPolygon = None
        self.agentlist: list[Agent] = []
        for agent in agentlist:
            self.add_agent(agent)

    def add_agent(self, agent: Agent):
        if agent not in self.agentlist:
            self.agentlist.append(agent)

grid_size = 1e-6