import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter
import binvox_rw
import numpy as np

def gml_to_binvox():
    outputData = []

    tree = etree.parse(inputDir)
    root = tree.getroot()
    '''
    if (root.tag.lower() != "gml"):
        print("Not a GML file.")
        return
    '''
    #~
    tag = root.find("tag")
    header = tag.find("header")
    drawing = tag.find("drawing")
    environment = header.find("environment")
    if not environment:
        environment = tag.find("environment")
    screenBounds = environment.find("screenBounds")
    #globalScale = (1.0,1.0,1.0)
    #dim = (float(screenBounds.find("x").text) * globalScale[0], float(screenBounds.find("y").text) * globalScale[1], float(screenBounds.find("z").text) * globalScale[2])
    dim = (40.0,40.0,40.0)
    #~
    strokes = drawing.findall("stroke")
    for stroke in strokes:
        pointsEl = stroke.findall("pt")
        for pointEl in pointsEl:
            x = float(pointEl.find("x").text) - 0.5
            y = float(pointEl.find("y").text) - 0.5
            z = float(pointEl.find("z").text) - 0.5
            time = float(pointEl.find("time").text)
            point = (x, y, z)
            outputData.append(point)
    
    '''
    # 2D example
    data = np.array([
        (0.1, 0.2, 0.3), (0.2, 0.3, 0.4), (0.3, 0.4, 0.1), (0.4, 0.1, 0.2),
        (0.2, 0.2, 0.2), (0.3, 0.3, 0.3), (0.4, 0.4, 0.4), (0.1, 0.1, 0.1),
        (0.3, 0.3, 0.3), (-2.0, 2.0, 0.4), (0.1, 0.1, 0.1), (0.2, 0.2, 0.2),
        (0.4, 0.4, 0.4), (2.45, 0.9, 0.9), (0.2, 0.2, 0.2), (0.1, 0.1, 0.1)
    ], np.float32)
    
    # 3D example
    data = np.array([
        [ [True, False, False, False], [False, True, False, False], [False, False, True, False], [False, False, False, True] ],
        [ [False, True, False, False], [False, False, True, False], [False, False, False, True], [True, False, False, False] ],
        [ [False, False, True, False], [False, False, False, True], [True, False, False, False], [False, True, False, False] ],
        [ [False, False, False, True], [True, False, False, False], [False, True, False, False], [False, False, True, False] ]
    ], np.bool)
    '''
    data = np.array([outputData], np.float32)
    if (data.ndim == 2):
        data.shape = (3,len(data))
    dims = [int(dim[0]), int(dim[0]), int(dim[0])] 
    translate = [0.0,0.0,0.0]
    scale = 40.0
    axis_order = "xyz"

    model = binvox_rw.Voxels(data, dims, translate, scale, axis_order)
      
    with open("test.binvox", "w") as f:
        print("Writing " + str(model.data.ndim) + "D array.")
        model.write(f)

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