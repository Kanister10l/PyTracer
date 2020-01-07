from LangEngine import LangEngine
from Engine3D import Engine3D
from ImageEngine import ImageEngine
from QuadTree import Node
from PathingEngine import PathingEngine
import json
import re

def ParseConfig(location):
    conf = json.load(open(location, "r"))
    imageSuffix = re.sub("^.*\/", "", conf["model_location"])[:-4]
    conf["tree_image_location"] = "./images/" + imageSuffix + "_tree_visualization.png"
    conf["map_image_location"] = "./images/" + imageSuffix + "_map_visualization.png"
    conf["path_output_file"] = "./output/" + imageSuffix + ".gcode"
    return conf


if __name__ == "__main__":
    conf = ParseConfig("./config/conf.json")
    engine3d = Engine3D()
    iengine = ImageEngine()
    engine3d.SetupEngine(conf["model_location"], cluster_size = conf["cluster_size"])
    engine3d.CalculateHeightMap(Xres = conf["map_resolution"])
    hmap = engine3d.NormalizeHeightMap(engine3d.heightMap)
    iengine.FromHeightMap(hmap, [engine3d.hmx, engine3d.hmy], scale = conf["image_scale"], location=conf["map_image_location"])
    tree = Node(None, Node.ROOT, {"map": hmap, "x_size": engine3d.hmx, "y_size": engine3d.hmy}, conf, 0)
    tree.SpawnNodes()
    iengine.FromTree(tree, [0, engine3d.hmx, 0, engine3d.hmy], scale = conf["image_scale"], location=conf["tree_image_location"])
    pth = PathingEngine(conf)
    pth.CreatePath(tree)
