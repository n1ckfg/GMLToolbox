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

# Tilt Brush license info:
# Copyright 2016 Google Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is sample Python 2.7 code that uses the tiltbrush.tilt module
to view raw Tilt Brush data."""

import os
import pprint
import sys

try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'Python'))
    from tiltbrush.tilt import Tilt
except ImportError:
    print >>sys.stderr, "Please put the 'Python' directory in your PYTHONPATH"
    sys.exit(1)

timeCounter = 0
timeIncrement = 0.01

def gmlHeader(dim=(1024,1024,1024)):
    s = "<gml spec=\"0.1b\">" + "\r"
    s += "\t<tag>" + "\r"
    s += "\t\t<header>" + "\r"
    s += "\t\t\t<client>" + "\r"
    s += "\t\t\t\t<name>TiltBrush</name>" + "\r"
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

def gmlStroke(points, color):
    s = "\t\t\t<stroke>" + "\r"
    s += "\t\t\t\t<brush>" + "\r"
    s += "\t\t\t\t\t<color>" + "\r"
    s += "\t\t\t\t\t\t<r>" + str(color[0]) + "</r>" + "\r"
    s += "\t\t\t\t\t\t<g>" + str(color[1]) + "</g>" + "\r"
    s += "\t\t\t\t\t\t<b>" + str(color[2]) + "</b>" + "\r"
    s += "\t\t\t\t\t\t<a>" + str(color[3]) + "</a>" + "\r"
    s += "\t\t\t\t\t</color>" + "\r"
    s += "\t\t\t\t</brush>" + "\r"
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
    
def dump_sketch(sketch, filename):
    globalScale = (-0.01, 0.01, 0.01)
    globalOffset = (0, 0, 0)
    useScaleAndOffset = True
    numPlaces = 7
    roundValues = True
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    sg = gmlHeader((512,512,512))
    allVals = []
    minVal = 0
    maxVal = 1
    for stroke in sketch.strokes:
    	for controlpoint in stroke.controlpoints:
    		for val in controlpoint.position:
    			allVals.append(val)
    allVals.sort()
    minVal = allVals[0]
    maxVal = allVals[len(allVals)-1]
    for stroke in sketch.strokes:
        color = (1,1,1)
        try:
            color = (stroke.brush_color[0], stroke.brush_color[1], stroke.brush_color[2], 1)
        except:
            pass
        points = []
        for controlpoint in stroke.controlpoints:
            point = controlpoint.position
            x = remap(point[0], minVal, maxVal, 0, 1)
            y = remap(point[1], minVal, maxVal, 0, 1)
            z = remap(point[2], minVal, maxVal, 0, 1)
            points.append((x,y,z))
        sg += gmlStroke(points, color)
    sg += gmlFooter()
	# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    """Prints out some rough information about the strokes.
    Pass a tiltbrush.tilt.Sketch instance."""
    '''
    cooky, version, unused = sketch.header[0:3]
    '''
    #output += 'Cooky:0x%08x    Version:%s    Unused:%s    Extra:(%d bytes)' % (
        #cooky, version, unused, len(sketch.additional_header))
    '''
    if len(sketch.strokes):
        stroke = sketch.strokes[0]    # choose one representative one
        def extension_names(lookup):
            # lookup is a dict mapping name -> idx
            extensions = sorted(lookup.items(), key=lambda (n,i): i)
            return ', '.join(name for (name, idx) in extensions)
        #output += "Stroke Ext: %s" % extension_names(stroke.stroke_ext_lookup)
        #if len(stroke.controlpoints):
            #output += "CPoint Ext: %s" % extension_names(stroke.cp_ext_lookup)
    '''
    '''
    for (i, stroke) in enumerate(sketch.strokes):
        #output += "%3d: " % i,
        output += dump_stroke(stroke)
    '''
    
    url = filename + ".gml"
    with open(url, "w") as f:
        f.write(sg)
        f.closed
        print("Wrote " + url)

def dump_stroke(stroke):
    strokeOutput = ""
    """Prints out some information about the stroke."""
    if len(stroke.controlpoints) and 'timestamp' in stroke.cp_ext_lookup:
        cp = stroke.controlpoints[0]
        for i in range(0, len(stroke.controlpoints)):
        	strokeOutput += str(i) + ". " + str(stroke.controlpoints[i].position) + "\n"
        timestamp = stroke.cp_ext_lookup['timestamp']
        start_ts = ' t:%6.1f' % (cp.extension[timestamp] * .001)
    else:
        start_ts = ''

    try:
        scale = stroke.extension[stroke.stroke_ext_lookup['scale']]
    except KeyError:
        scale = 1

    strokeOutput += "Brush: %2d    Size: %.3f    Color: #%02X%02X%02X %s    [%4d]" % (
        stroke.brush_idx, stroke.brush_size * scale,
        int(stroke.brush_color[0] * 255),
        int(stroke.brush_color[1] * 255),
        int(stroke.brush_color[2] * 255),
        #stroke.brush_color[3],
        start_ts,
        len(stroke.controlpoints))
    return strokeOutput + "\n"

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

def remap(value, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    valueScaled = float(value - min1) / float(range1)
    return min2 + (valueScaled * range2)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="View information about a .tilt")
    parser.add_argument('--strokes', action='store_true', help="Dump the sketch strokes")
    parser.add_argument('--metadata', action='store_true', help="Dump the metadata")
    parser.add_argument('files', type=str, nargs='+', help="Files to examine")

    args = parser.parse_args()
    if not (args.strokes or args.metadata):
        print "You should pass at least one of --strokes or --metadata"

    for filename in args.files:
        t = Tilt(filename)
        if args.strokes:
            dump_sketch(t.sketch, filename)
        if args.metadata:
            pprint.pprint(t.metadata)

if __name__ == '__main__':
    main()

