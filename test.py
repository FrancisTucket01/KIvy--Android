import mysql.connector

class conn():
    def __init__(self, *args):
        try:
            self.query = args[0]
        except IndexError as e:
            print("Index error")
        self.cone = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Tucket$693",
            database = "Colab"
        )
        
    def con(self, **kwargs):
        c = self.cone.cursor()
        try:
            if self.query:
                c.execute(self.query)
                return c
            else:
                return False
        except AttributeError as e:
            print("AttributeError")

        

s = "SELECT * FROM users"
x= conn(s)
r = x.con()
if r != None:
    for i in r:
        smt = f"SELECT * FROM messages WHERE sender='{i[1]}'"
        db = conn(smt)
        result= db.con()
        for o in result:
            print(o[2])