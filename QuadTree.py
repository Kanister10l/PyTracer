import math

class Node(object):
    ROOT = 0
    LEAF = 1
    BRANCH = 2

    def __init__(self, parent, node_type, area, environ, level):
        self.parent = parent
        self.node_type = node_type
        self.area = area
        self.environ = environ
        self.children = [None, None, None, None]
        self.level = level

    def VarRound(self, x):
        return round(x * (1 / self.environ["round_base"])) / (1 / self.environ["round_base"])
    
    def FindCommonHeight(self, ac):
        maxx = 0
        height = -1
        for k, v in ac.items():
            if (v > maxx and float(k) > height) or abs(float(k) - height) > self.environ["max_height_diff"]:
                maxx = v
                height = float(k)
        return [height, maxx]

    def NewBoundary(self, bound, x, y):
        return [min(bound[0], x), min(bound[1], y), max(bound[2], x), max(bound[3], y)]

    def CheckArea(self):
        bound = [float("inf"), float("inf"), 0, 0]
        step_size = [
            (self.area["map"][len(self.area["map"]) - 1][0] - self.area["map"][0][0]) / self.area["x_size"],
            (self.area["map"][len(self.area["map"]) - 1][1] - self.area["map"][0][1]) / self.area["y_size"]
        ]
        area_counter = {}
        for x in range(self.area["x_size"]):
            for y in range(self.area["y_size"]):
                bound = self.NewBoundary(bound, self.area["map"][x * self.area["y_size"] + y][0], self.area["map"][x * self.area["y_size"] + y][1])
                try:
                    area_counter[str(self.VarRound(self.area["map"][x * self.area["y_size"] + y][2]))] += 1
                except:
                    area_counter[str(self.VarRound(self.area["map"][x * self.area["y_size"] + y][2]))] = 1
        height_marker = self.FindCommonHeight(area_counter)
        if height_marker[1] / len(self.area["map"]) > (math.pi/4) - self.environ["area_error_factor"]:
            self.node_type = self.LEAF
            return True
        elif abs(bound[2] - bound[0]) <= 3 * self.environ["probe_diameter"] + step_size[0] or abs(bound[3] - bound[1]) <= 3 * self.environ["probe_diameter"] + step_size[1]:
            self.node_type = self.LEAF
            return True
        if self.node_type != self.ROOT:
            self.node_type = self.BRANCH
        return False

    def SpawnNodes(self):
        print("Spawn nodes on level: " + str(self.level))
        if self.CheckArea():
            return
        map1 = [[self.area["map"][x * self.area["y_size"] + y][0], self.area["map"][x * self.area["y_size"] + y][1], self.area["map"][x * self.area["y_size"] + y][2]] for x in range(int(self.area["x_size"] / 2)) for y in range(int(self.area["y_size"] / 2))]
        map2 = [[self.area["map"][x * self.area["y_size"] + y][0], self.area["map"][x * self.area["y_size"] + y][1], self.area["map"][x * self.area["y_size"] + y][2]] for x in range(int(self.area["x_size"] / 2)) for y in range(int(self.area["y_size"] / 2), self.area["y_size"])]
        map3 = [[self.area["map"][x * self.area["y_size"] + y][0], self.area["map"][x * self.area["y_size"] + y][1], self.area["map"][x * self.area["y_size"] + y][2]] for x in range(int(self.area["x_size"] / 2), self.area["x_size"]) for y in range(int(self.area["y_size"] / 2), self.area["y_size"])]
        map4 = [[self.area["map"][x * self.area["y_size"] + y][0], self.area["map"][x * self.area["y_size"] + y][1], self.area["map"][x * self.area["y_size"] + y][2]] for x in range(int(self.area["x_size"] / 2), self.area["x_size"]) for y in range(int(self.area["y_size"] / 2))]

        area1 = {
            "map": map1,
            "x_size": int(self.area["x_size"] / 2),
            "y_size": int(self.area["y_size"] / 2)
        }
        area2 = {
            "map": map2,
            "x_size": int(self.area["x_size"] / 2),
            "y_size": self.area["y_size"] - int(self.area["y_size"] / 2)
        }
        area3 = {
            "map": map3,
            "x_size": self.area["x_size"] - int(self.area["x_size"] / 2),
            "y_size": self.area["y_size"] - int(self.area["y_size"] / 2)
        }
        area4 = {
            "map": map4,
            "x_size": self.area["x_size"] - int(self.area["x_size"] / 2),
            "y_size": int(self.area["y_size"] / 2)
        }

        self.children[0] = Node(self, self.BRANCH, area1, self.environ, self.level + 1)
        self.children[0].SpawnNodes()
        self.children[1] = Node(self, self.BRANCH, area2, self.environ, self.level + 1)
        self.children[1].SpawnNodes()
        self.children[2] = Node(self, self.BRANCH, area3, self.environ, self.level + 1)
        self.children[2].SpawnNodes()
        self.children[3] = Node(self, self.BRANCH, area4, self.environ, self.level + 1)
        self.children[3].SpawnNodes()

    def WalkForArea(self, path):
        if self.node_type == self.LEAF:
            return [{
                "area": self.area,
                "path": path
            }]
        areas = []
        areas += self.children[0].WalkForArea(path + [0])
        areas += self.children[1].WalkForArea(path + [1])
        areas += self.children[2].WalkForArea(path + [2])
        areas += self.children[3].WalkForArea(path + [3])
        return areas