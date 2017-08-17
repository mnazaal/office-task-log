from flask import Flask, render_template, request
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence, CreateSequence
from datetime import datetime
from pytz import timezone
from math import ceil
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mnazaal'
db = SQLAlchemy(app)

class Logmessage(db.Model):
	__tablename__ = "logmessages"  #table name in postgres
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	message = db.Column(db.String(200)) #message posted
	user_name = db.Column(db.String(80))#, ForeignKey("logappuser.username")) #the user who posted the message

	def __init__(self, datetime, message, username):
		self.datetime = datetime
		self.message = message
		self.user_name = username

db.create_all() #creating the databases

@app.route("/")
def homepage():
	now = datetime.now()
	return render_template("index.html", messagelist=Logmessage.query.order_by(desc(Logmessage.datetime)).all()) #gets database items as an attribute

@app.route("/", methods = ['POST', 'GET'])  #changing view after a message is posted
def message_post():
	now = datetime.now()
	msgtext = request.form["messagebox"]  #enter the name attribute of form element within []
	if not(bool(re.match(r'^([ ]){0,}$', msgtext)) ) :  #regex which makes sure empty strings/spaces are not entered
		current_datetime = datetime.now(timezone("Indian/Maldives"))  #take time to be GMT+5
		data = Logmessage(current_datetime, str(msgtext), "nazaal") #must change username, taking it from external server
		db.session.add(data)
		db.session.commit()
		return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all())
	return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all())

@app.route("/", methods = ['POST', 'GET'])
def search_by_date():
    date = request.form["searchdate"]
    if (date != None):
        return render_template("index.html", filtered_data = Logmessage.query.order_by(desc(Logmessage.datetime)).filter(Logmessage.datetime.date() == datetime.today()))
    return render_template("index.html", filtered_data = Logmessage.query.order_by(desc(Logmessage.datetime)).filter(Logmessage.datetime.date() == datetime.today()))

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0")