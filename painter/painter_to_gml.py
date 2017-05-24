import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter

def painter_to_gml():
    outputFile = []

    file = readTextFile(inputDir)
    '''
    if (root.tag.lower() != "gml"):
        print("Not a GML file.")
        return
    '''
    #~
    outputFile.append(gmlHeader())
    file = file.splitlines(file.count("\r"))
    strokesEl = []
    strokeEl = []
    for line in file:
    	if (line.startswith("stroke_start")):
            strokeEl = []
        elif(line.startswith("pnt")):
        	strokeEl.append(line)
        elif(line.startswith("stroke_end")):
        	strokesEl.append(strokeEl)

    '''
    header = tag.find("header")
    drawing = tag.find("drawing")
    environment = header.find("environment")
    if not environment:
        environment = tag.find("environment")
    screenBounds = environment.find("screenBounds")
    globalScale = (1,1,1)
    dim = (float(screenBounds.find("x").text) * globalScale[0], float(screenBounds.find("y").text) * globalScale[1], float(screenBounds.find("z").text) * globalScale[2])
    #~
    outputFile.append(gmlHeader(dim))
    #~
    strokes = drawing.findall("stroke")
    for stroke in strokes:
        points = []
        pointsEl = stroke.findall("pt")
        for pointEl in pointsEl:
            x = float(pointEl.find("x").text) * dim[0] 
            y = float(pointEl.find("y").text) * dim[1]
            z = float(pointEl.find("z").text) * dim[2]
            time = float(pointEl.find("time").text)
            point = (x, y, z, time)
            points.append(point)
        outputFile.append(gmlStroke(points))
    '''
    outputFile.append(gmlFooter())
    writeTextFile(outputDir + "output.gml", outputFile)

def writeTextFile(name="test.txt", lines=None):
    file = open(name,"w") 
    for line in lines:
        file.write(line) 
    file.close() 

def readTextFile(name="text.txt"):
    file = open(name, "r") 
    return file.read() 

def remap(value, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    valueScaled = float(value - min1) / float(range1)
    return min2 + (valueScaled * range2)
    
def gmlHeader(dim=(1024,1024,1024)):
    s = "<gml spec=\"0.1b\">" + "\r"
    s += "\t<tag>" + "\r"
    s += "\t\t<header>" + "\r"
    s += "\t\t\t<client>" + "\r"
    s += "\t\t\t\t<name>KinectToPin</name>" + "\r"
    s += "\t\t\t</client>" + "\r"
    s += "\t\t\t<environment>" + "\r"
    s += "\t\t\t\t<up>" + "\r"
    s += "\t\t\t\t\t<x>0</x>" + "\r"
    s += "\t\t\t\t\t<y>1</y>" + "\r"
    s += "\t\t\t\t\t<z>0</z>" + "\r"
    s += "\t\t\t\t</up>" + "\r"
    s += "\t\t\t\t<screenBounds>" + "\r"
    s += "\t\t\t\t\t<x>" + str(dim[0]) + "</x>" + "\r"
    s += "\t\t\t\t\t<y>" + str(dim[1]) + "</y>" + "\r"
    s += "\t\t\t\t\t<z>" + str(dim[2]) + "</z>" + "\r"
    s += "\t\t\t\t</screenBounds>" + "\r"
    s += "\t\t\t</environment>" + "\r"
    s += "\t\t</header>" + "\r"
    s += "\t\t<drawing>" + "\r"
    return s

def gmlFooter():
    s = "\t\t</drawing>" + "\r"
    s += "\t</tag>" + "\r"
    s += "</gml>" + "\r"
    return s

def gmlStroke(points):
    s = "\t\t\t<stroke>" + "\r"
    for point in points:
        s += gmlPoint(point)
    s += "\t\t\t</stroke>" + "\r"
    return s

def gmlPoint(point):
    s = "\t\t\t\t<pt id=\"" + point[4] + "\">" + "\r"
    s += "\t\t\t\t\t<x>" + str(point[0]) + "</x>" + "\r"
    s += "\t\t\t\t\t<y>" + str(point[1]) + "</y>" + "\r"
    s += "\t\t\t\t\t<z>" + str(point[2]) + "</z>" + "\r"
    s += "\t\t\t\t\t<time>" + str(point[3]) + "</time>" + "\r"
    s += "\t\t\t\t</pt>" + "\r"
    return s

 # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

painter_to_gml()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~