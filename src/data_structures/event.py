class Event:
    """
    Represents a vertex event in Asano's rotational sweep algorithm.
    """
    def __init__(self, point: tuple[float, float], angle: float, dist2: float):
        self.point = point
        self.angle = angle
        self.dist2 = dist2
        self.start_edges = []
        self.end_edges = []

    def as_str(self):
        return f"Point: {self.point}, Angle: {self.angle}, Dist2: {self.dist2}"