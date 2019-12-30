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