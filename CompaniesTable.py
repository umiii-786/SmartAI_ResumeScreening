import mysql.connector
class Company():
    def __init__(self):
        self.conn=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
        )
        self.cursor=self.conn.cursor()
        self.cursor.execute('use ResumeSystem;')
    
    def getCompany(self,userid):
        self.cursor.execute(f"select * from Companies where userId='{userid}';")
        result=self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result
    
    def addCompany(self,cpid,clogo,Cname,About,userID):
        self.cursor.execute(f"insert into Companies (cpID,Clogo,Cname,About,userID) values ('{cpid}','{clogo}','{Cname}','{About}','{userID}') ;")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return
    

# cp=Company()
# cp.addCompany('6543','rew','ewqhgf','trewfd','nbvcxhgfd')



