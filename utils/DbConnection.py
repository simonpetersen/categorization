import sqlite3

class DbConnection:
    def __init__(self, databaseName):
        self.db = sqlite3.connect(databaseName)
        self.c = self.db.cursor()
    
    # Clean up the database. You do not need to change this function.
    def close(self):
        self.db.close()
        
    # This function should create the two tables registrations and models.
    # You can assume the tables do not exist.
    def createTables(self):
        sql = ["CREATE TABLE IF NOT EXISTS models(modelId INTEGER PRIMARY KEY, brand TEXT, maxSpeed REAL);", "CREATE TABLE IF NOT EXISTS registrations(carID TEXT PRIMARY KEY, modelId INTEGER, registrationYear INTEGER, price REAL, FOREIGN KEY(modelId) REFERENCES models(modelId));"]
        for i in sql:
            self.c.execute(i)
            self.db.commit()
    
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

    #XML Files
    def insertIntoXmlList(self, file):
        sql = "INSERT INTO XmlFiles (XmlFile, Name) VALUES(?,?);"
        self.c.execute(sql, (str(file),))
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


#registry = DbConnection("Database/WikiDB.sqlite")

#print(registry.getIgnoreList())