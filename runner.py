import utils.xmlparser
from categorizer import MRCategorizer
from utils.db import DbConnection

##### Files in DB #####
# - Batman
# - Superman
# - Obama
# - Game of Thrones

##### Read Xml from db
filename = "Obama"
connection = DbConnection("utils/WikiDB.sqlite")
file = connection.getXmlFile(filename)[1]
parser = utils.xmlparser.XmlParser(file)
text = parser.parse()
print("Article %s parsed." % filename)

##### Write parsed text to content-file
filelocation = "text-files/content.txt"
file = open(filelocation, 'w')
file.write(text)
file.close()

##### Generate categories
job = MRCategorizer(args=[filelocation])
with job.make_runner() as runner:
    runner.run()
    for key, value in job.parse_output(runner.cat_output()):
        print(value)
