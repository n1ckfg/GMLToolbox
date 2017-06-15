"use strict";

class Gml {

	constructor(data) {
        this.strokes = [];
        this.dim = [0,0,0];
        this.width = 0;
        this.height = 0;
        this.time = 0.0;
        this.timeOffset = 2.0;
        this.speed = 2.0;

        console.log(data.getChild("tag"));
        var header = data.children[0].children[0];
        var client = header.children[0];
        var environment = header.children[1];
        var up = environment.children[0];
        var screenBounds = environment.children[1];

        this.dim = [parseFloat(screenBounds.children[0].content), parseFloat(screenBounds.children[0].content), parseFloat(screenBounds.children[0].content)];
        this.width = parseInt(this.dim[0]);
        this.height = parseInt(this.dim[1]);

        var drawing = data.children[0].children[1];
        for (var i=0; i<drawing.children.length; i++) {
            var stroke = new GmlStroke(drawing.children[i], this.dim);
            this.strokes.push(stroke);
        }
    }

    update() {
        this.time = ((millis() / 1000.0)/(1.0/this.speed)) - this.timeOffset;
    }

    draw() {
        for (var i=0; i<this.strokes.length; i++) {
            this.strokes[i].time = this.time;
            this.strokes[i].draw();
        }
    }

    run() {
        this.update();
        this.draw();
    }

}

class GmlStroke {

    constructor(_strokeEl, _dim) {
        this.points = []
        this.time = 0;
        for (var i=0; i<_strokeEl.children.length; i++) {
            var pointEl = _strokeEl.children[i];
            var point = new GmlPoint(pointEl, _dim);
            this.points.push(point);
        }
	}

    draw() {
        beginShape();
        noFill();
        for (var i=0; i<this.points.length; i++) {
            if (this.points[i].time <= this.time) {
                strokeWeight(5);
                stroke(255, 200);
                vertex(this.points[i].pos.x, this.points[i].pos.y);
            }
        }
        endShape();
    }

}

class GmlPoint {

	constructor(_pointEl, _dim) {
        this.pos = createVector(parseFloat(_pointEl.children[0].content) * _dim[0], parseFloat(_pointEl.children[1].content) * _dim[1], parseFloat(_pointEl.children[2].content) * _dim[2]);
        this.time = parseFloat(_pointEl.children[3].content);
    }

}

function findElement(xml, name) {
	var returns;
	for (var i=0; i<xml.xmlElement.length; i++) {
		if (xml.xmlElement[i].tagName == name) {
			returns = xml.xmlElements[i];
			break;
		}
	}
	return returns;
}
