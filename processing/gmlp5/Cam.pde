// https://processing.org/reference/camera_.html
class Cam {

  PVector pos = new PVector(0,0,0);
  PVector poi = new PVector(0,0,0);
  PVector up = new PVector(0,0,0);

  Cam() {
    defaultPos();
    defaultPoi();
    defaultUp();
  }
  
  Cam(PVector _pos) {
    pos = _pos;
    defaultPoi();
    defaultUp();
  }
  
  Cam(PVector _pos, PVector _poi) {
    pos = _pos;
    poi = _poi;
    defaultUp();
  }
  
  Cam(PVector _pos, PVector _poi, PVector _up) {
    pos = _pos;
    poi = _poi;
    up = _up;
  }
  
  void update() {
    //
  }
  
  void draw() {
    camera(pos.x, pos.y, pos.z, poi.x, poi.y, poi.z, up.x, up.y, up.z);
  }
  
  void run() {
    update();
    draw();
  }
  
  void defaultPos() {
    pos.x = width/2.0;
    pos.y = height/2.0;
    pos.z = (height/2.0) / tan(PI*30.0 / 180.0);
  }
  
  void defaultPoi() {
    poi.x = width/2.0;
    poi.y = height/2.0;
    poi.z = 0;
  }
  
  void defaultUp() {
    up.x = 0;
    up.y = 1;
    up.z = 0;
  }
  
}

// TODO
// https://processing.org/reference/frustum_.html
// https://processing.org/reference/beginCamera_.html
// https://processing.org/reference/endCamera_.html