import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter
import binvox_rw
import numpy as np

def gml_to_binvox():
    outputFile = []

    tree = etree.parse(inputDir)
    root = tree.getroot()
    '''
    if (root.tag.lower() != "gml"):
        print("Not a GML file.")
        return
    '''
    #~
    '''
    tag = root.find("tag")
    header = tag.find("header")
    drawing = tag.find("drawing")
    environment = header.find("environment")
    if not environment:
        environment = tag.find("environment")
    screenBounds = environment.find("screenBounds")
    globalScale = (1,1,1)
    dim = (float(screenBounds.find("x").text) * globalScale[0], float(screenBounds.find("y").text) * globalScale[1], float(screenBounds.find("z").text) * globalScale[2])
    #~
    outputFile.append(painterHeader(dim))
    #~
    counter = 0
    strokes = drawing.findall("stroke")
    for stroke in strokes:
        points = []
        pointsEl = stroke.findall("pt")
        for pointEl in pointsEl:
            x = roundVal(float(pointEl.find("x").text) * dim[0], 2) 
            y = roundVal(float(pointEl.find("y").text) * dim[1], 2)
            z = roundVal(float(pointEl.find("z").text) * dim[2], 2)
            time = float(pointEl.find("time").text)
            point = (x, y, z, counter)
            counter += 1
            points.append(point)
        outputFile.append(painterStroke(points))
    outputFile.append(painterFooter())
    writeTextFile(outputDir + "output.txt", outputFile)
    '''
    data = np.array([
    	[[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5]],
    	[[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5]],
    	[[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5]],
    	[[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5],[0.5, 0.5, 0.5]]
    ], np.float32)
    print(data.dtype)
    dims = [4,4,4]
    translate = [0.0, 0.0, 0.0]
    scale = 40.0
    axis_order = "xyz"
    model = binvox_rw.Voxels(data, dims, translate, scale, axis_order)
    model.write(fp="test.binvox")

def writeTextFile(name="test.txt", lines=None):
    file = open(name,"w") 
    for line in lines:
        file.write(line) 
    file.close() 

def remap(value, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    valueScaled = float(value - min1) / float(range1)
    return min2 + (valueScaled * range2)

def roundVal(a, b):
    formatter = "{0:." + str(b) + "f}"
    return formatter.format(a)

def roundValInt(a):
    formatter = "{0:." + str(0) + "f}"
    return int(formatter.format(a))

 # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

gml_to_binvox()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~