from flask import Flask, render_template, request
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence, CreateSequence
from datetime import datetime
from math import ceil

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

@app.route("/", methods = ['POST'])
def message_post():
	message = None
	now = datetime.now()
	if (request.method == "POST") and (request.form["messagebox"] != ""):
		msgtext = request.form["messagebox"]  #enter the name attribute of form element within []
		data = Logmessage(datetime.utcnow(), str(msgtext), "nazaal") #must change username, taking it from external server
		db.session.add(data)
		db.session.commit()
		return render_template("index.html", messagelist=Logmessage.query.order_by(desc(Logmessage.datetime)).all())
	return render_template("index.html", messagelist=Logmessage.query.order_by(desc(Logmessage.datetime)).all())


if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0")