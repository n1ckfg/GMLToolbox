using System.Collections;
using System.Collections.Generic; 
using UnityEngine;
using System.Xml;
using System.Xml.Serialization;
using System.IO;

// http://wiki.unity3d.com/index.php?title=Saving_and_Loading_Data:_XmlSerializer

public class GMLContainer {

    //[XmlArray("Monsters"), XmlArrayItem("Monster")]
    //public Monster[] Monsters;

    public void Save(string path) {
        var serializer = new XmlSerializer(typeof(GMLContainer));
        using (var stream = new FileStream(path, FileMode.Create)) {
            serializer.Serialize(stream, this);
        }
    }

    public static GMLContainer Load(string path) {
        var serializer = new XmlSerializer(typeof(GMLContainer));
        using (var stream = new FileStream(path, FileMode.Open)) {
            return serializer.Deserialize(stream) as GMLContainer;
        }
    }

    //Loads the xml directly from the given string. Useful in combination with www.text.
    public static GMLContainer LoadFromText(string text) {
        var serializer = new XmlSerializer(typeof(GMLContainer));
        return serializer.Deserialize(new StringReader(text)) as GMLContainer;
    }

}
