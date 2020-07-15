from flask import Flask
from flask import render_template, redirect, url_for, session
from flask import request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
import json
from flask import jsonify
from flask_marshmallow import Marshmallow


app = Flask(__name__)

ma = Marshmallow(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "leave.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class EmpDetail(ma.Schema):
    class Meta:
        fields = ('id','email')

class LeaveDetail(ma.Schema):
    class Meta:
        fields = ('username','leave_type','leave_status','leave_creator','start_time','end_time','summary','total_leave_days','emp_id')

leave_detail = LeaveDetail(many=True)
emps_detail = EmpDetail(many=True)

class Employee(db.Model):
    def __init__(self,email):																																																																																																																																																																																																																																																																																																																																																																																																															
        self.email = email

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False,autoincrement=True)
    leave = db.relationship('Employee_leves', backref='employee', lazy=True)

remaining_leaves = 20
class Employee_leves(db.Model):
    def __init__(self,leave_type,leave_status,leave_creator,start_time,end_time,summary,total_leave_days,emp_id):
        self.leave_type = leave_type
        self.leave_status = leave_status
        self.leave_creator = leave_creator
        self.start_time = start_time
        self.end_time = end_time
        self.summary = summary
        self.total_leave_days = total_leave_days
        self.emp_id = emp_id

         
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    leave_type = db.Column(db.String(80), unique=False, nullable=False)
    leave_status = db.Column(db.String(80), unique=False, nullable=False)
    leave_creator = db.Column(db.String(80), unique=False, nullable=False)
    start_time = db.Column(db.String(80), unique=False, nullable=False)
    end_time = db.Column(db.String(80), unique=False, nullable=False)
    summary = db.Column(db.String(80), unique=False, nullable=False)
    total_leave_days = db.Column(db.Integer, unique=False, nullable=False)
    #remaining_leaves = remaining_leaves - total_leave_days
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)


@app.route("/home")  
def home():  
    return render_template("home.html")


@app.route("/statistic")  
def statistic():  
    return render_template("statistic.html")


@app.route("/update")  
def update():  
    con = sqlite3.connect("leave.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select email from employee;")
    #cur.execute("select * from id") 
    rows = cur.fetchall()  
    return render_template('update.html',rows=rows)
    return render_template("update.html")  




@app.route("/",methods=['GET','POST'])  
def index():  
    error = None
    #success = None
    if request.method == 'POST':
        if request.form['username'] != 'Priya Kawane' or request.form['password'] != 'admin':
            error = 'Invalid credentials Please try again.'
        else:
            success = 'Login successful!'
            return redirect(url_for('home'))
    return render_template("index.html",error=error)



@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/search')
def search_page():
    con = sqlite3.connect("leave.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select email from employee;")
    #cur.execute("select * from id") 
    rows = cur.fetchall()  
    return render_template('search.html',rows=rows)

    return render_template('search.html')


@app.route("/search", methods=["POST"])

def searchData():
    buf = request.data
    result = json.loads(buf.decode('utf-8'))
    if(result['name'] != ""):
        res = Employee.query.filter(Employee.email.contains(result['name']))
        result = emps_detail.dump(res)
    # data = {"some_key":"some_value"} # Your data in JSON-serializable type
        response = app.response_class(response = json.dumps(result),
                                    status=200,
                                    mimetype='application/json')
    else:
        response = app.response_class(response = json.dumps({"data":"no data"}),
                                    status=200,
                                    mimetype='application/json')

    return response

@app.route("/search/<emp_id>", methods=["GET"])
def getdata(emp_id):
    empid = Employee.query.get(id == emp_id)
    res = Employee_leves.query.filter(Employee_leves.emp_id == emp_id)
    result = leave_detail.dump(res)
    response = app.response_class(response = json.dumps(result),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route("/view")  
def view(): 
    con = sqlite3.connect("leave.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select email from employee;")
    #cur.execute("select * from id") 
    rows = cur.fetchall()  
    return render_template('view.html',rows=rows)
    return render_template("view.html")  


    
    '''
    con = sqlite3.connect("leave.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select username,summary,total_leave_days from employee_leves,information where username='Priya Kawane' and employee_leves.leave_creator = information.emailid;")
    #cur.execute("select * from id") 
    rows = cur.fetchall() ''' 
   
	
'''
class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)



@app.route("/")
def add():
        
    return render_template("home.html")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
        print(request.form)
    books = Book.query.all()
    return render_template("home.html", books=books)
'''

if __name__ == "__main__":
    app.run(debug=True)










