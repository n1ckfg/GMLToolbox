import sys as sys
import xml.etree.ElementTree as etree
from operator import itemgetter

def k2p_to_gml():
    outputFile = []

    tree = etree.parse(inputDir)
    root = tree.getroot()
    '''
    if (root.tag.lower() != "motioncapture"):
        print("Not a K2P XML file.")
        return
    '''
    #~
    globalScale = (1,1,1)
    globalScale = (globalScale[0] * float(root.attrib["width"]), globalScale[1] * float(root.attrib["height"]), globalScale[2] * float(root.attrib["depth"]))
    fps = float(root.attrib["fps"])
    #~
    outputFile.append(gmlHeader(globalScale))
    jointSelectionPoints = []
    #~
    mocapFrames = root.findall("MocapFrame")
    for mocapFrame in mocapFrames:
        frameNum = int(mocapFrame.attrib["index"])
        skeletons = mocapFrame.findall("Skeleton")
        for skeleton in skeletons:
            joints = skeleton.findall("Joints")
            for joint in joints:
                headEl = joint.find("head")
                neckEl = joint.find("neck")
                torsoEl = joint.find("torso")
                l_shoulderEl = joint.find("l_shoulder")
                l_elbowEl = joint.find("l_elbow")
                l_handEl = joint.find("l_hand")
                r_shoulderEl = joint.find("r_shoulder")
                r_elbowEl = joint.find("r_elbow")
                r_handEl = joint.find("r_hand")
                l_hipEl = joint.find("l_hip")
                l_kneeEl = joint.find("l_knee")
                l_footEl = joint.find("l_foot")
                r_hipEl = joint.find("r_hip")
                r_kneeEl = joint.find("r_knee")
                r_footEl = joint.find("r_foot")
                #~
                '''
                head = (float(headEl.attrib["x"]) * globalScale[0], float(headEl.attrib["y"]) * globalScale[1], float(headEl.attrib["z"]) * globalScale[2])
                neck = (float(neckEl.attrib["x"]) * globalScale[0], float(neckEl.attrib["y"]) * globalScale[1], float(neckEl.attrib["z"]) * globalScale[2])
                torso = (float(torsoEl.attrib["x"]) * globalScale[0], float(torsoEl.attrib["y"]) * globalScale[1], float(torsoEl.attrib["z"]) * globalScale[2])
                l_shoulder = (float(l_shoulderEl.attrib["x"]) * globalScale[0], float(l_shoulderEl.attrib["y"]) * globalScale[1], float(l_shoulderEl.attrib["z"]) * globalScale[2])
                l_elbow = (float(l_elbowEl.attrib["x"]) * globalScale[0], float(l_elbowEl.attrib["y"]) * globalScale[1], float(l_elbowEl.attrib["z"]) * globalScale[2])
                l_hand = (float(l_handEl.attrib["x"]) * globalScale[0], float(l_handEl.attrib["y"]) * globalScale[1], float(l_handEl.attrib["z"]) * globalScale[2])
                r_shoulder = (float(r_shoulderEl.attrib["x"]) * globalScale[0], float(r_shoulderEl.attrib["y"]) * globalScale[1], float(r_shoulderEl.attrib["z"]) * globalScale[2])
                r_elbow = (float(r_elbowEl.attrib["x"]) * globalScale[0], float(r_elbowEl.attrib["y"]) * globalScale[1], float(r_elbowEl.attrib["z"]) * globalScale[2])
                r_hand = (float(r_handEl.attrib["x"]) * globalScale[0], float(r_handEl.attrib["y"]) * globalScale[1], float(r_handEl.attrib["z"]) * globalScale[2])
                l_hip = (float(l_hipEl.attrib["x"]) * globalScale[0], float(l_hipEl.attrib["y"]) * globalScale[1], float(l_hipEl.attrib["z"]) * globalScale[2])
                l_knee = (float(l_kneeEl.attrib["x"]) * globalScale[0], float(l_kneeEl.attrib["y"]) * globalScale[1], float(l_kneeEl.attrib["z"]) * globalScale[2])
                l_foot = (float(l_footEl.attrib["x"]) * globalScale[0], float(l_footEl.attrib["y"]) * globalScale[1], float(l_footEl.attrib["z"]) * globalScale[2])
                r_hip = (float(r_hipEl.attrib["x"]) * globalScale[0], float(r_hipEl.attrib["y"]) * globalScale[1], float(r_hipEl.attrib["z"]) * globalScale[2])
                r_knee = (float(r_kneeEl.attrib["x"]) * globalScale[0], float(r_kneeEl.attrib["y"]) * globalScale[1], float(r_kneeEl.attrib["z"]) * globalScale[2])
                r_foot = (float(r_footEl.attrib["x"]) * globalScale[0], float(r_footEl.attrib["y"]) * globalScale[1], float(r_footEl.attrib["z"]) * globalScale[2])
                '''
                #~
                head = (float(headEl.attrib["x"]), float(headEl.attrib["y"]), float(headEl.attrib["z"]))
                neck = (float(neckEl.attrib["x"]), float(neckEl.attrib["y"]), float(neckEl.attrib["z"]))
                torso = (float(torsoEl.attrib["x"]), float(torsoEl.attrib["y"]), float(torsoEl.attrib["z"]))
                l_shoulder = (float(l_shoulderEl.attrib["x"]), float(l_shoulderEl.attrib["y"]), float(l_shoulderEl.attrib["z"]))
                l_elbow = (float(l_elbowEl.attrib["x"]), float(l_elbowEl.attrib["y"]), float(l_elbowEl.attrib["z"]))
                l_hand = (float(l_handEl.attrib["x"]), float(l_handEl.attrib["y"]), float(l_handEl.attrib["z"]))
                r_shoulder = (float(r_shoulderEl.attrib["x"]), float(r_shoulderEl.attrib["y"]), float(r_shoulderEl.attrib["z"])) 
                r_elbow = (float(r_elbowEl.attrib["x"]), float(r_elbowEl.attrib["y"]), float(r_elbowEl.attrib["z"]))
                r_hand = (float(r_handEl.attrib["x"]), float(r_handEl.attrib["y"]), float(r_handEl.attrib["z"]))
                l_hip = (float(l_hipEl.attrib["x"]), float(l_hipEl.attrib["y"]), float(l_hipEl.attrib["z"]))
                l_knee = (float(l_kneeEl.attrib["x"]), float(l_kneeEl.attrib["y"]), float(l_kneeEl.attrib["z"]))
                l_foot = (float(l_footEl.attrib["x"]), float(l_footEl.attrib["y"]), float(l_footEl.attrib["z"]))
                r_hip = (float(r_hipEl.attrib["x"]), float(r_hipEl.attrib["y"]), float(r_hipEl.attrib["z"]))
                r_knee = (float(r_kneeEl.attrib["x"]), float(r_kneeEl.attrib["y"]), float(r_kneeEl.attrib["z"]))
                r_foot = (float(r_footEl.attrib["x"]), float(r_footEl.attrib["y"]), float(r_footEl.attrib["z"]))
                #~
                time = (1.0/fps) * float(frameNum)
                head = (head[0], head[1], head[2], time, "head")
                neck = (neck[0], neck[1], neck[2], time, "neck")
                torso = (torso[0], torso[1], torso[2], time, "torso")
                l_shoulder = (l_shoulder[0], l_shoulder[1], l_shoulder[2], time, "l_shoulder")
                l_elbow = (l_elbow[0], l_elbow[1], l_elbow[2], time, "l_elbow")
                l_hand = (l_hand[0], l_hand[1], l_hand[2], time, "l_hand")
                r_shoulder = (r_shoulder[0], r_shoulder[1], r_shoulder[2], time, "r_shoulder")
                r_elbow = (r_elbow[0], r_elbow[1], r_elbow[2], time, "r_elbow")
                r_hand = (r_hand[0], r_hand[1], r_hand[2], time, "r_hand")
                l_hip = (l_hip[0], l_hip[1], l_hip[2], time, "l_hip")
                l_knee = (l_knee[0], l_knee[1], l_knee[2], time, "l_knee")
                l_foot = (l_foot[0], l_foot[1], l_foot[2], time, "l_foot")
                r_hip = (r_hip[0], r_hip[1], r_hip[2], time, "r_hip")
                r_knee = (r_knee[0], r_knee[1], r_knee[2], time, "r_knee")
                r_foot = (r_foot[0], r_foot[1], r_foot[2], time, "r_foot")
                #~
                points = [head, neck, torso, l_shoulder, l_elbow, l_hand, r_shoulder, r_elbow, r_hand, l_hip, l_knee, l_foot, r_hip, r_knee, r_foot]
                if (jointSelection == "all"):
                    outputFile.append(gmlStroke(points))
                else:
                    for point in points:
                        if (jointSelection == point[4]):
                            jointSelectionPoints.append(point)
    if (jointSelection != "all"):
        if (len(jointSelectionPoints) < 1):
            print("ERROR: Joint selection must be one of: ")
            print("all, head, neck, torso, l_shoulder, l_elbow, l_hand, r_shoulder, r_elbow, r_hand, l_hip, l_knee, l_foot, r_hip, r_knee, r_foot")
            return
        outputFile.append(gmlStroke(jointSelectionPoints))
    outputFile.append(gmlFooter())
    writeTextFile(outputDir + "output.gml", outputFile)

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
jointSelection = argv[2]

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

k2p_to_gml()

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~