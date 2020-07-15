from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import UserMixin
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///example.db'
app.config['SECREAT_KEY'] = 'mysecret'

db = 
 
@app.route('/')
def home():
		return "Hello World!"
 
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username']!= admin or 																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					request.form['password']!= admin:
			error = "Invalid credentials,Please try again"
		else:
			return redirect(url_for('home'))
	return render_template('login.html',error = error)
 
if __name__ == "__main__":
	app.run(debug=True)
