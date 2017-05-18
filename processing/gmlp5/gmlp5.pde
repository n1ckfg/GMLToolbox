XML xml;
ArrayList<PVector> points;
PVector dim;
Cam cam;

void setup() {
  size(50,50, P3D);
  
  xml = loadXML("example.gml");
  XML tag = xml.getChild("tag");
  XML header = tag.getChild("header");
  XML environment = tag.getChild("environment");
  XML screenBounds = environment.getChild("screenBounds");
  XML drawing = tag.getChild("drawing");
  XML[] stroke = drawing.getChildren("stroke");
  points = new ArrayList<PVector>();
  dim = new PVector();
  dim.x = screenBounds.getChild("x").getFloatContent();
  dim.y = screenBounds.getChild("y").getFloatContent();
  dim.z = screenBounds.getChild("z").getFloatContent();
  
  for (int i=0; i<stroke.length; i++) {
    XML[] pt = stroke[i].getChildren("pt");
    for (int j=0; j<pt.length; j++) {
      float x = pt[j].getChild("x").getFloatContent() * dim.x;
      float y = pt[j].getChild("y").getFloatContent() * dim.y;
      float z = pt[j].getChild("z").getFloatContent() * dim.z;
      points.add(new PVector(x,y,z));
    }
  }
  
  surface.setSize(int(dim.x), int(dim.y));
  cam = new Cam();
}

void draw() {
  background(0);
  
  for (int i=1; i<points.size(); i++) {
    PVector point1 = (PVector) points.get(i);
    PVector point2 = (PVector) points.get(i-1);
    strokeWeight(5);
    stroke(255);
    line(point1.x, point1.y, point1.z, point2.x, point2.y, point2.z);
  }
  
  updateControls();
  cam.run();
}