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