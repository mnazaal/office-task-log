from flask import Flask, render_template, request
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence, CreateSequence
from datetime import datetime
from math import ceil

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mnazaal'
db = SQLAlchemy(app)

#create database model, using SQLAlchemy
# class User(db.Model):
# 	__tablename__ = "logappuser"
# 	id = db.Column(db.Integer, primary_key=True, autoincrement=True)  #primary key
# 	username = db.Column(db.String(80), unique=True)  #username of mma user, note to grab this data from other source
# 	messages = relationship("Logmessage") #creating one to many relationship

# 	def __init__(self, id, username):
# 		self.id = id
# 		self.username = username
# 		self.messages = messages

# 	def __repr__(self, username):
# 		return '<Username %r' % self.username  #check this line
# 		return '<Message %r' % self.message #check this line

class Logmessage(db.Model):
	__tablename__ = "logmessages"
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	message = db.Column(db.String(200)) #message posted
	user_name = db.Column(db.String(80))#, ForeignKey("logappuser.username")) #the user who posted the message

	def __init__(self, datetime, message, username):
		self.datetime = datetime
		self.message = message
		self.user_name = username

	# def __repr__(self, message):
	# 	return '<Username %r' % self.username  #check this line
	# 	return '<Message %r' % self.message #check this line


db.create_all() #creating the databases


@app.route("/")
def homepage():
	now = datetime.now()
	return render_template("index.html", messagelist=Logmessage.query.all()) #gets database items as an attribute

@app.route("/", methods = ['POST'])
def message_post():
	message = None
	now = datetime.now()
	if request.method == "POST":
		msgtext = request.form["messagebox"]  #enter the name attribute of form element within []
		data = Logmessage(datetime.utcnow(), str(msgtext), "nazaal") #must change username, taking it from external server
		db.session.add(data)
		db.session.commit()
		return render_template("index.html", messagelist=Logmessage.query.all())






# 	HOW TO MAKE IT SHOW THE FORM FIELDS AND REAL TIME DATA
# 	return render_template("index.html")  #create HTML page here

# @app.route("/posted", methods = ['POST']) #add logpost number to url end
# def loghandler():
# 	username = None
# 	message = None
# 	if request.method == "POST":
# 		username = request.form['username'] #taking data from front-end form
# 		message = request.form['message']
# 		post = Log(username, message) #posting username and message to database
# 		db.session.add(post)
# 		db.session.commit()
# 		return render_template("index.html")
# 	return render_template("index.html")

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0")

