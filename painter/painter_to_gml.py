import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter

def painter_to_gml():
    outputFile = []
    fps = 60
    file = readTextFile(inputDir)
    '''
    if (root.tag.lower() != "gml"):
        print("Not a GML file.")
        return
    '''
    #~
    file = file.splitlines(file.count("\r"))
    firstTime = 0.0
    strokesEl = []
    strokeEl = []
    painterHeader = ""
    for line in file:
        if (line.startswith("new_3")):
            painterHeader = line
        elif (line.startswith("stroke_start")):
            strokeEl = []
        elif(line.startswith("pnt")):
            strokeEl.append(line)
        elif(line.startswith("stroke_end")):
            strokesEl.append(strokeEl)
        else:
            pass
    
    dim = (640, 480, 0)
    if (painterHeader):
        dim = extractPainterDim(painterHeader)

    outputFile.append(gmlHeader(dim))

    for strokeEl in strokesEl:
        points = []
        for pointEl in strokeEl:
            point = extractPainterLine(pointEl)
            if (point):
                if (firstTime == 0.0):
                    firstTime = point[3]
                point = (point[0]/dim[0], point[1]/dim[1], 0.0, (point[3] - firstTime) * 1.0/float(fps))
                points.append(point)
        outputFile.append(gmlStroke(points))

    outputFile.append(gmlFooter())
    writeTextFile(outputDir + "output.gml", outputFile)

def extractPainterLine(line):
    returns = line.split(" ")
    for s in returns:
        if (s==""):
            returns.remove(s)
    try:
        returns = (float(returns[2]), float(returns[4]), 0.0, float(returns[6]))
        return returns
    except:
        return None

def extractPainterDim(line):
    returns = line.split(" ")
    for s in returns:
        if (s==""):
            returns.remove(s)
    try:
        returns = (float(returns[3]), float(returns[5]), 0.0)
        return returns
    except:
        return None    

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
    s += "\t\t\t\t<name>CorelPainter</name>" + "\r"
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
    #s = "\t\t\t\t<pt id=\"" + point[4] + "\">" + "\r"
    s = "\t\t\t\t<pt>" + "\r"
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