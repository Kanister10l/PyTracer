from LangEngine import LangEngine
from Engine3D import Engine3D
from ImageEngine import ImageEngine

engine3d = Engine3D()
iengine = ImageEngine()
engine3d.SetupEngine("rb3.stl", cluster_size = 2000)
engine3d.CalculateHeightMap(Xres = 1920)
iengine.FromHeightMap(engine3d.heightMap, [engine3d.hmx, engine3d.hmy], scale = 1)