import sqlite3

class DbConnection:
    def __init__(self, database_name):
        self.db = sqlite3.connect(database_name)
        self.c = self.db.cursor()
    
    # Clean up the database. You do not need to change this function.
    def close(self):
        self.db.close()
    
    #IgnoreList
    def getIgnoreList(self):
        sql = "SELECT * FROM IgnoreList;"
        self.c.execute(sql)
        values = self.c.fetchall()
        resultArr = []
        for i in values:
            resultArr.append(i[1])
        return resultArr

    def insertIntoList(self, arr):
        sql = "INSERT INTO IgnoreList (Value) VALUES (?);"
        for i in arr:
            self.c.execute(sql,(str(i),))
        self.db.commit()

    def wordIsInIgnoreList(self, word):
        sql = "SELECT * FROM IgnoreList WHERE Value = ?"
        self.c.execute(sql, (word,))
        result = self.c.fetchone()
        self.db.commit()
        return result is not None

    #XML Files
    def insertIntoXmlList(self, file, name):
        sql = "INSERT INTO XmlFiles (XmlFile, Name) VALUES(?,?);"
        self.c.execute(sql, (str(file), str(name)))
        self.db.commit()

    def getAllXmlFiles(self):
        sql = "SELECT * FROM XmlFiles;"
        self.c.execute(sql)
        values = self.c.fetchall()
        resultArr = []
        for i in values:
            resultArr.append([i[1], i[2]])
        return resultArr

    def getXmlFile(self, fileName):
        sql = "SELECT * FROM XmlFiles WHERE Name = ?;"
        self.c.execute(sql, (fileName,))
        value = self.c.fetchone()

        return value

#Initialize connection
#registry = DbConnection("WikiDB.sqlite")

#Insert into stoplist
#registry.insertIntoList(['new'])

#Insert into XmlFiles
'''
with open('text-files/batman.xml', 'r') as myfile:
    data=myfile.read().replace('\n', '')
registry.insertIntoXmlList(data, "Batman")
'''