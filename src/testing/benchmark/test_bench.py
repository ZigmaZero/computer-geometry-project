from testing.inputs.input_generation import build_random_input
import numpy as np

class TestBench:
    def __init__(self, region_x: float,
                       region_y: float,
                       obstacle_count: int,
                       obstacle_vertex_min: int,
                       obstacle_vertex_max: int,
                       faction_count: int,
                       agent_count: int):
        self.region_x = region_x
        self.region_y = region_y
        self.obstacle_count = obstacle_count
        self.obstacle_vertex_min = obstacle_vertex_min
        self.obstacle_vertex_max = obstacle_vertex_max
        self.faction_count = faction_count
        self.agent_count = agent_count

    def bench(self, repetitions: int = 20):
        times = []
        for i in range(repetitions):
            testinput = build_random_input(self.region_x, self.region_y,
                                           self.obstacle_count,
                                           self.obstacle_vertex_min,
                                           self.obstacle_vertex_max,
                                           self.faction_count, self.agent_count)
            time = testinput.run_test()
            print(f"{i+1}/{repetitions}: {time[0]:.6f}, {time[1]:.6f}")
            times.append(time)

        baseline = [t[0] for t in times]
        proposed = [t[1] for t in times]

        print("=== Results ===")
        print(f"Baseline Average: {np.mean(baseline):.6f} seconds")
        print(f"Baseline Standard Deviation: {np.std(baseline):.6f} seconds")
        print(f"Proposed Average: {np.mean(proposed):.6f} seconds")
        print(f"Proposed Standard Deviation: {np.std(proposed):.6f} seconds")
