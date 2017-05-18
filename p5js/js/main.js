"use strict";

var gml;

function preload() {
  loadXML("./files/example.gml", function(data) {
      gml = new Gml(data);
  });
}

function setup() {
	createCanvas(gml.width, gml.height);
}

function draw(){
	background(0);
  gml.run();
}

