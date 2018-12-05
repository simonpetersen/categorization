import utils.xmlparser
from categorizer import MRCategorizer
from utils.db import DbConnection

connection = DbConnection("utils/WikiDB.sqlite")
list_of_articles = connection.getAllXmlFiles()
article_names = list(map(lambda a: a[1], list_of_articles))
print('#### Available articles:')
for n in article_names:
    print(n)
print('#####')
line = input('Write the name of the article you want to categorize: ')
while line not in article_names:
    line = input('Invalid article. Please try again: ')

##### Extract text from xml
file = list(filter(lambda a: a[1] == line, list_of_articles))[0][0]
parser = utils.xmlparser.XmlParser(file)
text = parser.parse()
print("Article %s parsed." % line)

##### Write text to content-file
filelocation = "text-files/content.txt"
file = open(filelocation, 'w')
file.write(text)
file.close()

##### Generate categories
job = MRCategorizer(args=[filelocation])
with job.make_runner() as runner:
    runner.run()
    for key, value in job.parse_output(runner.cat_output()):
        print(key)
