Cam cam;
Gml gml;

void setup() {
  size(50, 50, P3D);
  gml = new Gml("example.gml");
  surface.setSize(gml.width, gml.height);
  cam = new Cam();
}

void draw() {
  background(0);
  updateControls();
  gml.run();
  cam.run();
}