from flask import Flask,render_template,request,session,make_response
import mysql.connector
import os 
import numpy as np
import uuid
from flask import abort, redirect, url_for
from descriptionAnalyzer.CheckDescription import ProcessDescription
from descriptionAnalyzer.CalculatePerfection import PerfectionScore
from CompaniesTable import Company
from werkzeug.utils import secure_filename
from JobTable import JobPost

# from flask_jwt_extended import create_access_token,JWTManager,jwt_required,get_current_user,set_access_cookies
app=Flask(__name__)
app.config['UPLOAD_FOLDER']="./upload/"
conn=mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
)



@app.route('/')
def HomePage():
    # if request.cookies.get('token'):
    return render_template('home.html')
    # else:
    #     return redirect(url_for('LoginPage'))

@app.route('/login',methods=['Get','POST'])
def LoginPage():
    
    if request.method=="POST":
        password=request.form['Password']
        email=request.form['email']
        if not email or not password:
            return "email or password is empty"
        
        # print(email,'  ',password)
        cr=conn.cursor()
        cr.execute('use ResumeSystem;') 
        cr.execute(f"select * from User where email='{email}' and password='{password}';")
        result=cr.fetchone()
        cp=Company()
        check=cp.getCompany(result[0])
        Is_company="False"
        if check!=None:Is_company="True"
        response=make_response(redirect(url_for('JobsScreen')))
        response.set_cookie('token',result[0])
        response.set_cookie('Is_company',Is_company)
        return response
    else:
        return render_template('login.html')

@app.route('/checkUserInDB',methods=["POST"])
def checkUserInDB():
    urlForCheck=request.form['check']
    if  urlForCheck=="register":
        email=request.form['email']
        res=HelpDB({'email':email})

    else:
        password=request.form['Password']
        email=request.form['email']
        print('in the check user')
        res=HelpDB({'email':email,'password':password})
    return res
        

def HelpDB(checkData):
    print('in the help db user')
    prefix="select * from User where "
    count=1
    for keys, value in checkData.items():
        if count==2:
            prefix+=" and "
        prefix+=f"{keys}='{value}'"
        count=count+1
    prefix+=";"
    cr=conn.cursor()
    cr.execute('use ResumeSystem;')
    print('hn ya run hoi',prefix)
    cr.execute(prefix)
    result = cr.fetchone()
    print(result)
    cr.close()
    if not result:
        return "null"
    else:
        return 'notNull'

@app.route('/register',methods=['GET','POST'])
def RegisterPage():

    if request.method=="POST":
        cr=conn.cursor()
        cr.execute('use ResumeSystem;') 
        username=request.form['Username']
        password=request.form['Password']
        email=request.form['email']
        # print(username,password,email)
        id=uuid.uuid4()
        id=str(id)
        # print(f"INSERT INTO User (id,username, email, password) VALUES ('{id}','{username}', '{email}', '{password}');")
        cr.execute(f"INSERT INTO User (id,username, email, password) VALUES ('{id}','{username}', '{email}', '{password}');")
        conn.commit()
        return redirect(url_for('LoginPage'))
    return render_template('register.html')

@app.route('/jobs')
def JobsScreen():
    if request.cookies.get('token') and request.cookies.get('Is_company'):
        userid=request.cookies.get('token')
        return render_template('JobListing.html',id=userid)
    else:
        return redirect(url_for('LoginPage'))

@app.route('/user/<id>')
def MainScreen(id):
    # if request.cookies.get('Is_company'):
    Is_company=request.cookies.get('Is_company')
    companyInfo=""
    jobsPost=""
    if Is_company=="True":
        cp=Company()
        companyInfo=cp.getCompany(id)
        jb=JobPost()
        jobsPost=jb.getAllJobPost(cpId=companyInfo[0])
        
        print(companyInfo)
    print(jobsPost)
    return render_template('studentDashboard.html',
                           id=id,
                           jobsPost=jobsPost,
                           Is_company=Is_company,
                           companyInfo=companyInfo)

@app.route('/user/<id>/company',methods=["POST"])
def createCompany(id):
    cp=Company()
    exist=cp.getCompany(id)
    print(exist)
    if exist!=None:
        return 'this Company is Already registered'
    else:
        if request.files and request.form:
            logo=request.files['Clogo']
            logoname=secure_filename(logo.filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'],logoname)
            logo.save(path)
            cp=Company()
            cpid=str(uuid.uuid4())
            cp.addCompany(cpid,logo.filename,request.form['Cname'],request.form['Cabout'],id)
            print('added company in table ')
            response=make_response(redirect(f"/user/{id}"))
            response.set_cookie('Is_company',"True")
            return response
        else: 
            return 'data is not available'
    # return 'received'
    
@app.route('/company/<cpid>/job',methods=['POST','GET'])
def createJob(cpid):
    jobid=uuid.uuid4()
    jobid=str(jobid)
    print(jobid)
    jobTitle=request.form['jobTitle']
    loc=request.form['loc']
    jobDesc=request.form['Jobdesc']
    
    print(jobid,'\n',jobTitle,'\n',jobDesc,'\n',loc,'\n',cpid)
    jb=JobPost()
    jb.addJobPost(jobid,cpid,jobTitle,loc,jobDesc)
    res=make_response(redirect(f'/user/{request.cookies.get('token')}'))
    return res




@app.route('/signout',methods=["GET"])
def signoutUser():
    res=make_response(redirect('/login'))
    res.set_cookie('token','',expires=0)
    res.set_cookie('Is_company','',expires=0)
    return res



@app.route('/AnalyzeDesc',methods=['POST'])
def AnalyzeDescription():
   data=request.form['description']
   category=ProcessDescription([data])
   score=PerfectionScore(category,[data])
#    print(score)
#    print(category)
   answers=[]
   answers.append(category)
   answers.append(score)
   return answers
    


if __name__=="__main__":
    app.run(port=80,debug=True)