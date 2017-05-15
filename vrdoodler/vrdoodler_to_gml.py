#!/usr/bin/env python

'''
The Lightning Artist Toolkit was developed with support from:
   Canada Council on the Arts
   Eyebeam Art + Technology Center
   Ontario Arts Council
   Toronto Arts Council
   
Copyright (c) 2016 Nick Fox-Gieg
http://fox-gieg.com
'''

'''
VRDoodler license info:
CREATIVE COMMONS
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)
https://creativecommons.org/licenses/by-nc-sa/4.0/
'''

import os
import pprint
import sys

'''
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'Python'))
    from tiltbrush.tilt import Tilt
except ImportError:
    print >>sys.stderr, "Please put the 'Python' directory in your PYTHONPATH"
    sys.exit(1)
'''

timeCounter = 0
timeIncrement = 0.01

def rgbIntToTuple(rgbint, normalized=False):
    rgbVals = [ rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256 ]
    if (normalized == True):
    	for i in range(0, len(rgbVals)):
    		c = float(rgbVals[i]) / 255.0
    		rgbVals[i] = c;
    return (rgbVals[2], rgbVals[1], rgbVals[0])

def roundVal(a, b):
    formatter = "{0:." + str(b) + "f}"
    return formatter.format(a)

def checkForZero(v):
	hitRange = 0.005
	if (abs(v[0]) < hitRange and abs(v[1]) < hitRange and abs(v[2]) < hitRange):
		return True
	else:
		return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert a VRDoodler .obj")
    #parser.add_argument('--strokes', action='store_true', help="Dump the strokes")
    #parser.add_argument('--metadata', action='store_true', help="Dump the metadata")
    parser.add_argument('files', type=str, nargs='+', help="Files to examine")

    args = parser.parse_args()
    #if not (args.strokes or args.metadata):
        #print "You should pass at least one of --strokes or --metadata"

    for filename in args.files:
        save_gp(filename)

def gmlHeader(dim=(1024,1024,1024)):
    s = "<gml spec=\"0.1b\">" + "\r"
    s += "\t<tag>" + "\r"
    s += "\t\t<header>" + "\r"
    s += "\t\t\t<client>" + "\r"
    s += "\t\t\t\t<name>KinectToPin</name>" + "\r"
    s += "\t\t\t</client>" + "\r"
    s += "\t\t</header>" + "\r"
    s += "\t\t<environment>" + "\r"
    s += "\t\t\t<up>" + "\r"
    s += "\t\t\t\t<x>0</x>" + "\r"
    s += "\t\t\t\t<y>1</y>" + "\r"
    s += "\t\t\t\t<z>0</z>" + "\r"
    s += "\t\t\t</up>" + "\r"
    s += "\t\t\t<screenBounds>" + "\r"
    s += "\t\t\t\t<x>" + str(dim[0]) + "</x>" + "\r"
    s += "\t\t\t\t<y>" + str(dim[1]) + "</y>" + "\r"
    s += "\t\t\t\t<z>" + str(dim[2]) + "</z>" + "\r"
    s += "\t\t\t</screenBounds>" + "\r"
    s += "\t\t</environment>" + "\r"
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
    global timeCounter
    global timeIncrement
    s = "\t\t\t\t<pt>" + "\r"
    s += "\t\t\t\t\t<x>" + str(point[0]) + "</x>" + "\r"
    s += "\t\t\t\t\t<y>" + str(point[1]) + "</y>" + "\r"
    s += "\t\t\t\t\t<z>" + str(point[2]) + "</z>" + "\r"
    s += "\t\t\t\t\t<time>" + str(timeCounter) + "</time>" + "\r"
    s += "\t\t\t\t</pt>" + "\r"
    timeCounter += timeIncrement
    return s

def save_gp(filename):
    globalScale = (10, 10, 10)
    globalOffset = (0, 0, 0)
    useScaleAndOffset = True
    numPlaces = 7
    roundValues = True
    
    with open(filename) as data_file: 
        data = data_file.readlines()
    strokes = []
    points = []
    for line in data:
        if str(line).startswith("l") == True:
            if (len(points) > 0):
                strokes.append(points)
                points = []
        elif str(line).startswith("v") == True:
            pointRaw = line.split()
            point = (-1 * float(pointRaw[1]), float(pointRaw[2]), float(pointRaw[3]))
            points.append(point)
    print("Read " + str(len(strokes)) + " strokes.")

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    sg = gmlHeader((512,512,512))
    for i in range(0,len(strokes)):
        sg += gmlStroke(strokes[i])
    sg += gmlFooter()
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    url = filename + ".gml"
    with open(url, "w") as f:
        f.write(sg)
        f.closed
        print("Wrote " + url)    

if __name__ == '__main__':
    main()