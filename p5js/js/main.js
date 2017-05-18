"use strict";

var screenBounds, drawing, up;
var width, height, depth;
var strokes = [];
var points = [];

function preload() {
	loadXML("./files/example.gml", function(data) {
		var header = data.children[0].children[0];
		var client = header.children[0];
		//~
		var environment = data.children[0].children[1];
		up = environment.children[0];
		screenBounds = environment.children[1];
		//~
		drawing = data.children[0].children[2];
	});
}

function setup() {
	width = screenBounds.children[0].content;
	height = screenBounds.children[1].content
	createCanvas(width, height);

	for (var i=0; i<drawing.children.length; i++) {
		strokes.push(drawing.children[i]);
	}

	for (var i=0; i<strokes.length; i++) {
		for (var j=0; j<strokes[i].children.length; j++) {
			var pointEl = strokes[i].children[j];
			point = createVector(pointEl.children[0].content, pointEl.children[1].content, pointEl.children[2].content)
			point.x *= width;
			point.y *= height;
			point.z *= depth;
			points.push(point);
		}
	}
}

function draw(){
	background(0,0,0);

	for (var i=1; i<points.length; i++) {
		strokeWeight(5);
		stroke(255, 127);
		line(points[i].x, points[i].y, points[i-1].x, points[i-1].y);
		strokeWeight(1);
		stroke(255);
		line(points[i].x, points[i].y, points[i-1].x, points[i-1].y);
	}
}

class Gml {
	constructor() {

	}
}

class GmlStroke {
	constructor() {

	}
}

class GmlPoint {
	constructor() {

	}
}

/*
class Gml {
  
  XML xml;
  ArrayList<GmlStroke> strokes;
  PVector dim;
  int width;
  int height;
  String fileName;
  float time;
  float timeOffset = 3.0;
  float speed = 2.0;

  Gml() {
    strokes = new ArrayList<GmlStroke>();
    // TODO
    // width = screen width
    // height = screen height
    // fileName = filename to save
  }
  
  Gml(String _fileName) {
    time = 0;
    fileName = _fileName;
    xml = loadXML(fileName);
    XML tag = xml.getChild("tag");
    XML header = tag.getChild("header");
    XML environment = tag.getChild("environment");
    XML screenBounds = environment.getChild("screenBounds");
    dim = new PVector();
    dim.x = screenBounds.getChild("x").getFloatContent();
    dim.y = screenBounds.getChild("y").getFloatContent();
    dim.z = screenBounds.getChild("z").getFloatContent();
    width = int(dim.x);
    height = int(dim.y);

    XML drawing = tag.getChild("drawing");
    XML[] strokesEl = drawing.getChildren("stroke");
    strokes = new ArrayList<GmlStroke>();
    
    for (int i=0; i<strokesEl.length; i++) {
      GmlStroke stroke = new GmlStroke(strokesEl[i], dim);
      strokes.add(stroke);
    }  
  }
  
  void update() {
    time = ((float(millis()) / 1000.0)/(1.0/speed)) - timeOffset;
  }
  
  void draw() {
    for (int i=0; i<strokes.size(); i++) {
      GmlStroke stroke = strokes.get(i);
      stroke.time = time;
      stroke.draw();
    }
  }
  
  void run() {
    update();
    draw();
  }
  
}

class GmlStroke {
  
  ArrayList<GmlPoint> points;
  float time;

  GmlStroke() {
    points = new ArrayList<GmlPoint>();
  }

  GmlStroke(XML _xml, PVector _dim) {
    time = 0;
    XML[] pt = _xml.getChildren("pt");
    points = new ArrayList<GmlPoint>();
    for (int i=0; i<pt.length; i++) {
      GmlPoint point = new GmlPoint(pt[i], _dim);
      points.add(point);
    }
  }
  
  void draw() {
    for (int i=1; i<points.size(); i++) {
      GmlPoint point1 = points.get(i);
      GmlPoint point2 = points.get(i-1);
      if (point1.time <= time) {
        strokeWeight(5);
        stroke(255);
        line(point1.pos.x, point1.pos.y, point1.pos.z, point2.pos.x, point2.pos.y, point2.pos.z);
      }
    }
  }
  
}

class GmlPoint {
  
  PVector pos;
  float time;
  
  GmlPoint(PVector _pos) {
    pos = _pos;
    time = float(millis())/1000.0;
  }
  
  GmlPoint(XML _xml, PVector _dim) {
    float x = _xml.getChild("x").getFloatContent() * _dim.x;
    float y = _xml.getChild("y").getFloatContent() * _dim.y;
    float z = _xml.getChild("z").getFloatContent() * _dim.z;
    pos = new PVector(x,y,z);
    time = _xml.getChild("time").getFloatContent();
  }
  
}
*/