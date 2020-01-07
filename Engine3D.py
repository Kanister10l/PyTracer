import numpy
import stl
from shapely.geometry import LineString, Polygon
from stl import mesh
from progress.bar import Bar

class Engine3D(object):
    polys = None
    my_mesh = None
    planes = None
    Xmax = None
    Xmin = None
    Ymax = None
    Ymin = None
    heightMap = None
    hmx = None
    hmy = None
    clusters = None
    clusterBase = None
    clusterStep = None

    def LoadMesh(self, location):
        print("Loading mesh from 3D file")
        self.my_mesh = mesh.Mesh.from_file(location)
        print("3D mesh sucessfully loaded")

    def ConvertMeshToPolygons(self):
        print("Converting plane vertices to polygons")
        self.polys = []
        to_do = len(self.my_mesh.points)
        bar = Bar('Converting', max=to_do, suffix='%(percent)d%%')
        for p in self.my_mesh.points:
            self.polys.append(Polygon([[p[0], p[1]], [p[3], p[4]], [p[6], p[7]]]))
            bar.next()
        bar.finish()

    def CalculatePlanes(self):
        print("Calculating planes from polygons")
        self.planes = []
        to_do = len(self.polys)
        bar = Bar('Calculating', max=to_do, suffix='%(percent)d%%')
        for i in range(len(self.polys)):
            if self.polys[i].is_valid:
                d = self.my_mesh.normals[i][0]*self.my_mesh.points[i][0] + self.my_mesh.normals[i][1]*self.my_mesh.points[i][1] + self.my_mesh.normals[i][2]*self.my_mesh.points[i][2]
                self.planes.append([self.my_mesh.normals[i][0], self.my_mesh.normals[i][1], self.my_mesh.normals[i][2], d])
                bar.next()
            else:
                self.planes.append(None)
                bar.next()
        bar.finish()

    def GetDimensions(self):
        minx = None
        maxx = None
        miny = None
        maxy = None
        for p in self.my_mesh.points:
            if minx is None:
                minx = p[stl.Dimension.X]
                maxx = p[stl.Dimension.X]
                miny = p[stl.Dimension.Y]
                maxy = p[stl.Dimension.Y]
            else:
                maxx = max(p[stl.Dimension.X], maxx)
                minx = min(p[stl.Dimension.X], minx)
                maxy = max(p[stl.Dimension.Y], maxy)
                miny = min(p[stl.Dimension.Y], miny)
        self.Xmax = maxx
        self.Xmin = minx
        self.Ymax = maxy
        self.Ymin = miny

    def InitClusers(self, k = 5):
        self.clusters = []
        for _ in range(k**2):
            self.clusters.append([])
        self.clusterStep = [(self.Xmax - self.Xmin) / k, (self.Ymax - self.Ymin) / k]
        self.clusterBase = k

    def FindPolyBox(self, points):
        minX = points[0]
        maxX = points[0]
        minY = points[1]
        maxY = points[1]
        minX = min(minX, points[3])
        minX = min(minX, points[6])
        maxX = max(maxX, points[3])
        maxX = max(maxX, points[6])
        minY = min(minY, points[4])
        minY = min(minY, points[7])
        maxY = max(maxY, points[4])
        maxY = max(maxY, points[7])
        return [minX, maxX, minY, maxY]

    def AssignClusters(self, polyNumber):
        poly = self.my_mesh.points[polyNumber]
        box = self.FindPolyBox(poly)
        fromX = int((box[0] - self.Xmin) / self.clusterStep[0])
        toX = int((box[1] - self.Xmin) / self.clusterStep[0])
        fromY = int((box[2] - self.Ymin) / self.clusterStep[1])
        toY = int((box[3] - self.Ymin) / self.clusterStep[1])
        if toX == self.clusterBase:
            toX -=1
        if toY == self.clusterBase:
            toY -=1
        for x in range(fromX, toX + 1):
            for y in range(fromY, toY + 1):
                self.clusters[x*self.clusterBase + y].append(polyNumber)
        
    def ClusterifyPolygons(self):
        print("Assigning polygons to clusters")
        to_do = len(self.polys)
        bar = Bar('Calculating', max=to_do, suffix='%(percent)d%%')
        for i in range(to_do):
            self.AssignClusters(i)
            bar.next()
        bar.finish()

    def SetupEngine(self, location, cluster_size = 5):
        self.LoadMesh(location)
        self.ConvertMeshToPolygons()
        self.CalculatePlanes()
        self.GetDimensions()
        self.InitClusers(k = cluster_size)
        self.ClusterifyPolygons()

    def CalculateZValue(self, index, x, y):
        return (self.planes[index][3] - self.planes[index][0] * x - self.planes[index][1] * y) / self.planes[index][2]
    
    def FindCluster(self, x, y):
        cx = int((x - self.Xmin) / self.clusterStep[0])
        cy = int((y - self.Ymin) / self.clusterStep[1])
        return cx * self.clusterBase + cy

    def Intersect(self, x, y):
        z = float("-inf")
        cluster = self.FindCluster(x, y)
        l = LineString([[x - 0.0000001, y - 0.0000001], [x, y]])
        for i in self.clusters[cluster]:
            if self.polys[i].is_valid and l.intersects(self.polys[i]):
                z = max(self.CalculateZValue(i, x, y), z)
        return z

    def CalculateHeightMap(self, Xres = 1920):
        print("Calculating height map")
        self.heightMap = []
        dX = self.Xmax - self.Xmin
        dY = self.Ymax - self.Ymin
        Yres = int((dY * Xres) / dX)
        self.hmx = Xres
        self.hmy = Yres
        stepX = dX / (Xres + 1)
        stepY = dY / (Yres + 1)
        bar = Bar('Calculating', max=Xres*Yres, suffix='%(percent)d%%')
        for x in range(Xres):
            for y in range(Yres):
                self.heightMap.append([self.Xmin + (x + 1) * stepX, self.Ymin + (y + 1) * stepY, self.Intersect(self.Xmin + (x + 1) * stepX, self.Ymin + (y + 1) * stepY)])
                bar.next()
        bar.finish()
    
    def NormalizeHeightMap(self, hmap):
        minx = float("inf")
        miny = float("inf")
        minz = float("inf")
        for point in hmap:
            minx = min(point[0], minx)
            miny = min(point[1], miny)
            if point[2] != float("-inf"):
                minz = min(point[2], minz)
        offx = 0.0 - minx
        offy = 0.0 - miny
        offz = 0.0 - minz
        newmap = []
        for i in range(len(hmap)):
            if hmap[i][2] != float("-inf"):
                newmap.append([hmap[i][0] + offx, hmap[i][1] + offy, hmap[i][2] + offz])
            else:
                newmap.append([hmap[i][0] + offx, hmap[i][1] + offy, 0.0])
        return newmap