using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LADrawing : MonoBehaviour {

    public LightningArtist latk;
	public BrushStroke brushPrefab;
    public enum BrushMode { ADD, ALPHA };
    public BrushMode brushMode = BrushMode.ADD;
    public Color color = new Color(1f, 0f, 0f);
	public float brushSize = 0.05f;
	public float minDistance = 0f;

    [HideInInspector] public int gridRows = 10;
    [HideInInspector] public int gridColumns = 10;
    [HideInInspector] public float gridCell = 0.1f;

    void Awake() {
        if (!latk) latk = GetComponent<LightningArtist>();
        if (latk) {
            brushPrefab = latk.brushPrefab;
            color = latk.mainColor;
            brushSize = latk.brushSize;
        }
    }

    void Start () {
		//makeGrid(0f, gridCell);
	}

    public void makeGrid(float zPos, float cell) {
		float xMax = (float) gridRows * cell;
		float yMax = (float) gridColumns * cell;
		float xHalf = xMax / 2f;
		float yHalf = yMax / 2f;

		for (int x=0; x<=gridRows; x++) {
			float xPos = (float) x * cell;
			makeLine(new Vector3(-xHalf, xPos-xHalf, zPos), new Vector3(xHalf, xPos-xHalf, zPos));
		}

		for (int y=0; y<=gridColumns; y++) {
			float yPos = (float) y * cell;
			makeLine(new Vector3(yPos-yHalf, -yHalf, zPos), new Vector3(yPos-yHalf, yHalf, zPos));
		}
	}

    public void makeLine(Vector3 v1, Vector3 v2) {
		BrushStroke brush = Instantiate(brushPrefab);
		brush.transform.SetParent(transform);

		brush.points.Add(v1);
		brush.points.Add(v2);
		brush.brushColor = color;
		brush.brushSize = brushSize;
	}

    public void makeCurve(List<Vector3> points) {
    	if (minDistance > 0f) points = filterMinDistance(points);
        BrushStroke brush = null;
        if (latk) {
            latk.inputInstantiateStroke(color, points);
        } else {
            brush = Instantiate(brushPrefab);
            brush.transform.SetParent(transform);
            brush.brushMode = (BrushStroke.BrushMode)brushMode;
            brush.points = points;
            brush.brushColor = color;
            brush.brushSize = brushSize;
        }
    }

    public List<Vector3> filterMinDistance(List<Vector3> points) {
        List<Vector3> returns = new List<Vector3>();
        //returns.Add(points[0]);
        for (int i=1; i<points.Count; i++) {
            if (Vector3.Distance(points[i], points[i-1]) >= minDistance) {
                returns.Add(points[i]);
            }
        }
        return returns;
    }

}
