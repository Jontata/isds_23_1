import xml.sax

class MyHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print("startElement", name)

    def endElement(self, name):
        print("endElement", name)

    def characters(self, content):
        print("characters", content[:60])  # Print the first 60 characters

path = r'W:\extract\Ejendomsvurdering_Totaludtraek_Flad_Complete_Restricted_XML_20230730000021.xml'
parser = xml.sax.make_parser()
parser.setContentHandler(MyHandler())
parser.parse(path)
