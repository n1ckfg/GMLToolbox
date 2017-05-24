import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter

def gml_to_painter():
    outputFile = []

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
    globalScale = (1,1,1)
    dim = (float(screenBounds.find("x").text) * globalScale[0], float(screenBounds.find("y").text) * globalScale[1], float(screenBounds.find("z").text) * globalScale[2])
    #~
    outputFile.append(painterHeader(dim))
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
        outputFile.append(painterStroke(points))
    outputFile.append(painterFooter())
    writeTextFile(outputDir + "output.txt", outputFile)

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
    
def painterHeader(dim=(1024,1024,1024)):
    s = "script_version_number version 10" + "\r"
    s += "artist_name \"\"" + "\r"
    s += "start_time date Wed, May 24, 2017 time 3:23 PM" + "\r"
    s += "start_random 1366653360 1884255589" + "\r"
    s += "variant \"Painter Brushes\" \"F-X\" \"Big Wet Luscious\"" + "\r"
    s += "max_size_slider   14.00000" + "\r"
    s += "min_radius_fraction_slider    0.20599" + "\r"
    s += "build" + "\r"
    s += "penetration_slider 100 percent" + "\r"
    s += "texture \"Paper Textures\" \"<str t=17500 i=001>\"" + "\r"
    s += "grain_inverted unchecked" + "\r"
    s += "directional_grain unchecked" + "\r"
    s += "scale_slider    1.00000" + "\r"
    s += "paper_brightness_slider    0.50000" + "\r"
    s += "paper_contrast_slider    1.00000" + "\r"
    s += "portfolio_change \"\"" + "\r"
    s += "gradation \"Painter Gradients.gradients\" \"<str t=17503 i=001>\"" + "\r"
    s += "weaving \"Painter Weaves.weaves\" \"<str t=17504 i=001>\"" + "\r"
    s += "pattern_change \"Painter Patterns\" \"<str t=17001 i=001>\"" + "\r"
    s += "path_library_change \"Painter Selections\"" + "\r"
    s += "nozzle_change \"Painter Nozzles\" \"<str t=17000 i=001>\"" + "\r"
    s += "use_brush_grid unchecked" + "\r"
    s += "new_tool 1" + "\r"
    s += "gradation_options type 0 order 0 angle    0.00 spirality  1.000" + "\r"
    s += "pattern_options pattern_type 1 offset 0.594" + "\r"
    s += "preserve_transparency unchecked" + "\r"
    s += "wind_direction 4.712389" + "\r"
    s += "color red 1 green 109 blue 255" + "\r"
    s += "background_color red 255 green 4 blue 4" + "\r"
    s += "change_file \"ntitled-1\"" + "\r"
    s += "new_3 \"Untitled-1\" width " + str(dim[0]) + " height " + str(dim[1]) + " resolution   72.00000 width_unit 1 height_unit 1 resolution_unit 1 paper_color red 255 green 255 blue 255 movie 0 frames 1" + "\r"
    return s

def painterFooter():
    s = "end_time date Wed, May 24, 2017 time 3:25 PM" + "\r"
    return s

def painterStroke(points):
    s = "stroke_start" + "\r"
    for point in points:
        s += gmlPoint(point)
    s += "stroke_end" + "\r"
    return s

def gmlPoint(point):
    x = point[0]
    y = point[1]
    time = point[3]
    s = "pnt x " + str(x) + " y " + str(y) + " time " + str(time) + " prs 1.00 tlt 0.00 brg 0.00 whl 1.00 rot 0.00" + "\r"
    return s

 # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

gml_to_painter()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~