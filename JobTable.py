import mysql.connector
class JobPost():
    def __init__(self):
        self.conn=mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
        )
        self.cursor=self.conn.cursor()
        self.cursor.execute('use ResumeSystem;')
    
    def getParticularJob(self,jobId):
        self.cursor.execute(f"select * from  JobPost where jobId='{jobId}';")
        result=self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        return result
    
    def addJobPost(self,cpId,jobId,jobTitle,loc,jobDesc):
        self.cursor.execute(f"insert into JobPost (jobId,jobTitle,loc,jobDesc,cpId) values ('{jobId}','{jobTitle}','{loc}','{jobDesc}','{cpId}') ;")
        # print('queery running ')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        return
    
    def getAllJobPost(self,cpId=""):
        if  cpId=="":
            print('not khali wali')
            self.cursor.execute("select * from JobPost;")
        else:
            self.cursor.execute(f"select * from JobPost where cpId='{cpId}';")
        result=self.cursor.fetchmany()
        self.cursor.close()
        self.conn.close()
        return result
    

# jb=JobPost()

# jb.addJobPost('8765432','7654321','helloworld','nawabshah','hi where are you  ')

# cp=Company()
# cp.addCompany('6543','rew','ewqhgf','trewfd','nbvcxhgfd')



