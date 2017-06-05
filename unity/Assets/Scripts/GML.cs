using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GML {
    public Vector3 screenBounds = Vector3.one;
    public Vector3 up = new Vector3(0f, 1f, 0f);
    public List<GMLStroke> strokes = new List<GMLStroke>();
}

public class GMLStroke {
    public List<GMLPoint> points = new List<GMLPoint>();

    public List<Vector3> getPoints() {
        List<Vector3> returns = new List<Vector3>();
        for (int i = 0; i < points.Count; i++) {
            returns.Add(points[i].pt);
        }
        return returns;
    }
}

public class GMLPoint {
    public Vector3 pt = Vector3.zero;
    public float time = 0f;
}