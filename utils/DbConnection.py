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
    
    def getIgnoreList(self):
        sql = "SELECT * FROM IgnoreList;"
        values = self.c.fetchall()
        resultArr = []
        for i in values:
            resultArr.append(i[1])
        return resultArr

    def insertIntoList(self, arr):
        sql = "INSERT INTO IgnoreList (Value) VALUES (?);"
        for i in arr:
            self.c.execute("INSERT INTO IgnoreList (Value) VALUES (?);",(str(i),))
        self.db.commit()

registry = DbConnection("Database/WikiDB.sqlite")
