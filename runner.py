import utils.xmlparser
from categorizer import MRCategorizer
from categorizer import MRCategorizerAll
from utils.db import DbConnection

connection = DbConnection("utils/WikiDB.sqlite")
list_of_articles = connection.getAllXmlFiles()
article_names = list(map(lambda a: a[1], list_of_articles))
article_names = article_names + ['All']
print('#### Available articles:')
for n in article_names:
    print(n)
print('#####')
line = input('Write the name of the article you want to categorize: ')
while line.lower() not in [x.lower() for x in article_names]:
    line = input('Invalid article. Please try again: ')

if(line.lower() == 'all'):
    files = []
    for entry in list_of_articles:
        parser = utils.xmlparser.XmlParser(entry[0])
        text = parser.parse()
        filelocation = "text-files/Parsed_Files/content." + entry[1] + ".txt"
        file = open(filelocation, 'w', encoding="UTF-8")
        file.write(text)
        file.close
        files.append(filelocation)
    print("All Articles parsed.")
    job = MRCategorizerAll(args=files)
    with job.make_runner() as runner:
        runner.run()
        counter = 1
        print('Following categorization can be suggested for the articles')
        for key, value in job.parse_output(runner.cat_output()):
            category_name = key.split(':')[-1]
            list_of_files = key.split(':')[:-1]
            list_of_names = []
            for file in list_of_files:
                filename = file.split('.')[1:-1]
                list_of_names.append(filename)
            category_spaces =  ' ' * int(2 - int(counter/10))
            print(str(counter) + category_spaces + 'Category: ' + category_name)
            for i in list_of_names:
                print(' | ' + i[0], end = '')
            print(' | ')
            counter = counter + 1


else:
    ##### Extract text from xml
    file = list(filter(lambda a: a[1].lower() == line.lower(), list_of_articles))[0][0]
    parser = utils.xmlparser.XmlParser(file)
    text = parser.parse()
    print("Article %s parsed." % line)

    ##### Write text to content-file
    filelocation = "text-files/content.txt"
    file = open(filelocation, 'w', encoding="UTF-8")
    file.write(text)
    file.close()

    ##### Generate categories
    job = MRCategorizer(args=[filelocation])
    with job.make_runner() as runner:
        runner.run()
        print('The following categories can be suggested for this article:')
        counter = 1
        for key, value in job.parse_output(runner.cat_output()):
            category_spaces =  ' ' * int(2 - int(counter/10))
            print(str(counter) + ':' + category_spaces + key)
            counter = counter + 1
