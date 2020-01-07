from LangEngine import LangEngine

class PathingEngine(object):
    
    def __init__(self, environ):
        super().__init__()
        self.environ = environ
        self.safeHeight = 0.0
        self.probeSize = self.environ["probe_diameter"]
        self.interval = self.environ["measure_interval"]
        self.lang = LangEngine()
        self.lang.InitEngine(self.environ["language_descriptor_location"])

    def FindMaxZ(self, areas):
        z = 0.0
        for area in areas:
            for point in area["area"]["map"]:
                z = max(point[2], z)
        return z

    def Round(self, n):
        return round(n, ndigits=self.environ["path_round_digits"])

    def RoundAreas(self, areas):
        for i in range(len(areas)):
            for j in range(len(areas[i]["area"]["map"])):
                areas[i]["area"]["map"][j][0] = self.Round(areas[i]["area"]["map"][j][0])
                areas[i]["area"]["map"][j][1] = self.Round(areas[i]["area"]["map"][j][1])
                areas[i]["area"]["map"][j][2] = self.Round(areas[i]["area"]["map"][j][2])
        return areas
    
    def GenericMove(self, **kwargs):
        if self.environ["default_move_type"] == "rapid":
            self.lang.RapidMove(**kwargs)
        elif self.environ["default_move_type"] == "linear":
            self.lang.LinearMove(**kwargs)

    def FindMeasureHeight(self, area):
        z = 0.0
        for point in area["area"]["map"]:
            z = max(point[2], z)
        return z + self.environ["measure_height"]

    def AnalyzeArea(self, area):
        bbox = [
            area["area"]["map"][0][0], # MIN X
            area["area"]["map"][0][1], # MIN Y
            area["area"]["map"][len(area["area"]["map"]) - 1][0], # MAX X
            area["area"]["map"][len(area["area"]["map"]) - 1][1]  # MAX Y
        ]

        x_steps = int((bbox[2] - bbox[0] - self.probeSize) / self.interval)
        y_steps = int((bbox[3] - bbox[1] - self.probeSize) / self.interval)
        print(bbox[2] - bbox[0], bbox[3] - bbox[1])
        x_offset = self.probeSize / 2 + ((bbox[2] - bbox[0] - self.probeSize) - float(x_steps) * self.interval)
        y_offset = self.probeSize / 2 + ((bbox[3] - bbox[1] - self.probeSize) - float(y_steps) * self.interval)
        z_height = self.FindMeasureHeight(area)
        forward = False
        self.GenericMove(
            x = bbox[0] + x_offset,
            y = bbox[1] + y_offset,
            z = self.safeHeight)
        for iy in range(y_steps):
            forward = not forward
            for ix in range(x_steps):
                tx = ix
                if not forward:
                    tx = x_steps - 1 - ix
                self.GenericMove(
                    x = bbox[0] + x_offset + tx * self.interval,
                    y = bbox[1] + y_offset + iy * self.interval,
                    z = z_height)
                self.lang.Pause()
        self.GenericMove(z = self.safeHeight)


    def CreatePath(self, tree):
        self.lang.SetAbsolute()
        self.lang.SetMilimeters()

        areas = self.RoundAreas(tree.WalkForArea([]))

        self.safeHeight = self.FindMaxZ(areas) + self.environ["z_hop"]
        self.GenericMove(x = 0.0, y = 0.0, z = self.safeHeight)

        for area in areas:
            self.AnalyzeArea(area)
        self.lang.SaveCode(self.environ["path_output_file"])