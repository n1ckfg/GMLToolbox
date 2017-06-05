using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Xml;

public class GMLDraw : MonoBehaviour {

    public LightningArtist latk;
    public LADrawing latkd;
    public enum GMLMode { READ_STILL, READ_DRAW, WRITE };
    public GMLMode gmlMode = GMLMode.READ_STILL;
    public string fileName;
    public Vector3 globalScale = new Vector3(0.01f, 0.01f, 0.01f);

    [HideInInspector] public GML gml;

    private XmlDocument xml; 
    private string url;

	void Start() {
        url = Application.dataPath + "/StreamingAssets/" + fileName;
        StartCoroutine(LoadGML(url));
    }

    void Update() {
		
	}

    // https://forum.unity3d.com/threads/xml-reading-a-xml-file-in-unity-how-to-do-it.44441/

    IEnumerator LoadGML(string url) {
        GML gml = new GML();
        xml = new XmlDocument();
        xml.Load(url);
        yield return xml;
        XmlNode root = xml.FirstChild;

        XmlNode tag = root["tag"];
        XmlNode header = tag["header"];
        XmlNode environment = header["environment"];
        XmlNode up = environment["up"];
        XmlNode screenBounds = environment["screenBounds"];
        gml.screenBounds.x = float.Parse(screenBounds["x"].InnerText) * globalScale.x;
        gml.screenBounds.y = float.Parse(screenBounds["y"].InnerText) * globalScale.y;
        gml.screenBounds.z = float.Parse(screenBounds["z"].InnerText) * globalScale.z;
        Debug.Log("dim: " + gml.screenBounds);

        XmlNode drawing = tag["drawing"];
        for (int i=0; i<drawing.ChildNodes.Count; i++) {
            GMLStroke stroke = new GMLStroke();
            XmlNode strokeEl = drawing.ChildNodes[i];
            for (int j=0; j<strokeEl.ChildNodes.Count; j++) {
                XmlNode pt = strokeEl.ChildNodes[j];
                float x = float.Parse(pt["x"].InnerText) * gml.screenBounds.x;
                float y = float.Parse(pt["y"].InnerText) * gml.screenBounds.y;
                float z = float.Parse(pt["z"].InnerText) * gml.screenBounds.z;
                float time = float.Parse(pt["time"].InnerText);
                GMLPoint point = new GMLPoint();
                point.pt = new Vector3(x, y, z);
                point.time = time;
                stroke.points.Add(point);
            }
            gml.strokes.Add(stroke);
        }

        for (int i=0; i<gml.strokes.Count; i++) {
            latkd.makeCurve(gml.strokes[i].getPoints());
        }
    }

    public class GML {
        public Vector3 screenBounds = Vector3.one;
        public Vector3 up = new Vector3(0f, 1f, 0f);
        public List<GMLStroke> strokes = new List<GMLStroke>();
    }

    public class GMLStroke {
        public List<GMLPoint> points = new List<GMLPoint>();

        public List<Vector3> getPoints() {
            List<Vector3> returns = new List<Vector3>();
            for (int i=0; i<points.Count; i++) {
               returns.Add(points[i].pt);
            }
            return returns;
        }
    }

    public class GMLPoint {
        public Vector3 pt = Vector3.zero;
        public float time = 0f;
    }

}
