from flask import Flask,render_template,request
import ast 
app=Flask(__name__)

@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/login')
def LoginPage():
    return render_template('login.html')

@app.route('/register')
def RegisterPage():
    return render_template('register.html')

@app.route('/student')
def MainScreen():
    return render_template('studentDashboard.html')

@app.route('/AnalyzeDesc',methods=['POST'])
def AnalyzeDescription():
   print('request ao')
   data=request.form['description']
   print(data)
#    data=ast.literal_eval(data)

#    print(data)
   return "ok"
    


if __name__=="__main__":
    app.run(port=80,debug=True)