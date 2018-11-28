import utils.xmlparser
from utils.db import DbConnection

filename = "Batman"
connection = DbConnection("utils/WikiDB.sqlite")
file = connection.getXmlFile(filename)[1]
parser = utils.xmlparser.XmlParser(file)
text = parser.parse()
print("File %s parsed." % filename)

filelocation = "text-files/content.txt"
file = open(filelocation, 'w')
file.write(text)
file.close()
