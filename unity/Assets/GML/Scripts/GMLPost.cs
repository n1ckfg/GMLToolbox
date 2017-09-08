using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class GMLPost : MonoBehaviour {

    public GMLDraw gmlDraw;
    public string url = "http://000000book.com/data";
    public string appName = "Unity";

    private void Awake() {
        if (gmlDraw == null) gmlDraw = GetComponent<GMLDraw>();
    }

    private void Start() {
		
	}
	
	private void Update() {
		if (Input.GetKeyDown(KeyCode.Space)) {
            if (gmlDraw.loaded) {
                StartCoroutine(postToBook());
            } else {
                Debug.Log("GML not ready yet.");
            }
        }
	}

    // https://github.com/jamiew/blackbook/wiki/Upload-GML-to-000000book
    // https://docs.unity3d.com/Manual/UnityWebRequest-SendingForm.html
    /*
    keywords (string) [comma-separated list of keywords (‘tags’, not to be confused w/ graf tags)]
    location (string) [name like ‘NYC’, lat/long coordinates, or even a URL]
    username (string) [a 000000book user’s login]
    author (string) [the person who was actually writing]
    */

    private IEnumerator postToBook() {
        List<IMultipartFormSection> formData = new List<IMultipartFormSection>();
        //formData.Add(new MultipartFormDataSection("field1=foo&field2=bar"));
        //formData.Add(new MultipartFormFileSection("my file data", "myfile.txt"));

        string s = gmlDraw.xml.ToString();
        formData.Add(new MultipartFormDataSection("gml=" + gmlDraw.xml.ToString() + "&application=" + appName));
        Debug.Log(s);
        UnityWebRequest www = UnityWebRequest.Post(url, formData);
        yield return www.Send();

        if (www.isNetworkError) {
            Debug.Log(www.error);
        } else {
            Debug.Log("Form upload complete!");
        }
    }

}
