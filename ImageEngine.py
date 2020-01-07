from PIL import Image

class ImageEngine(object):
    outImage = None

    def FromHeightMap(self, hMap, res, scale = 1, location = "image.png"):
        print("Generating image")
        minz = float("inf")
        maxz = float("-inf")
        for i in hMap:
            if i[2] != float("-inf"):
                minz = min(minz, i[2])
                maxz = max(maxz, i[2])
        delta = maxz - minz
        norm = []
        for i in hMap:
            if i[2] != float("-inf"):
                norm.append(int((maxz - i[2]) / delta * 255))
            else:
                norm.append(255)
        im= Image.new("RGB", (res[0] * scale, res[1] * scale), "#FFFFFF")
        for x in range(res[0]):
            for y in range(res[1]):
                im.paste((norm[x*res[1] + y], norm[x*res[1] + y], norm[x*res[1] + y]), (x*scale, y*scale, x*scale + scale, y*scale + scale))
        im.save(location)

    def DivideRes(self, res, option):
        if option == 0:
            fromx = res[0]
            tox = res[0] + int((res[1] - res[0]) / 2)
            fromy = res[2]
            toy = res[2] + int((res[3] - res[2]) / 2)
            return [fromx, tox, fromy, toy]
        if option == 1:
            fromx = res[0]
            tox = res[0] + int((res[1] - res[0]) / 2)
            fromy = res[2] + int((res[3] - res[2]) / 2)
            toy = res[3]
            return [fromx, tox, fromy, toy]
        if option == 2:
            fromx = res[0] + int((res[1] - res[0]) / 2)
            tox = res[1]
            fromy = res[2] + int((res[3] - res[2]) / 2)
            toy = res[3]
            return [fromx, tox, fromy, toy]
        if option == 3:
            fromx = res[0] + int((res[1] - res[0]) / 2)
            tox = res[1]
            fromy = res[2]
            toy = res[2] + int((res[3] - res[2]) / 2)
            return [fromx, tox, fromy, toy]

    def FromTree(self, tree, res, scale = 1, location = "tree.png"):
        print("Generating image")
        minz = float("inf")
        maxz = float("-inf")
        areas = tree.WalkForArea([])
        for area in areas:
            for i in area["area"]["map"]:
                minz = min(minz, i[2])
                maxz = max(maxz, i[2])
        delta = maxz - minz
        im= Image.new("RGB", (res[1] * scale, res[3] * scale), "#FFFFFF")
        for area in areas:
            subres = res
            for opt in area["path"]:
                subres = self.DivideRes(subres, opt)
            for x in range(subres[0], subres[1]):
                for y in range(subres[2], subres[3]):
                    im.paste((int((maxz - area["area"]["map"][(x - subres[0])*(subres[3] - subres[2]) + (y - subres[2])][2]) / delta * 255), int((maxz - area["area"]["map"][(x - subres[0])*(subres[3] - subres[2]) + (y - subres[2])][2]) / delta * 255), int((maxz - area["area"]["map"][(x - subres[0])*(subres[3] - subres[2]) + (y - subres[2])][2]) / delta * 255)), (x*scale, y*scale, x*scale + scale, y*scale + scale))
            im.paste((0, 255, 0), (subres[0]*scale, subres[2]*scale, subres[0]*scale + 1, subres[3]*scale))
            im.paste((0, 255, 0), (subres[0]*scale, subres[2]*scale, subres[1]*scale, subres[2]*scale + 1))
            im.paste((0, 255, 0), (subres[1]*scale, subres[2]*scale, subres[1]*scale - 1, subres[3]*scale))
            im.paste((0, 255, 0), (subres[0]*scale, subres[3]*scale, subres[1]*scale, subres[3]*scale - 1))
        im.save(location)