from flask import Flask, render_template, request
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, desc, Date, cast
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence, CreateSequence
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, date, time
from pytz import timezone
from math import ceil
import re
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mnazaal'
db = SQLAlchemy(app)

class Logmessage(db.Model):
	__tablename__ = "logmessages"  #table name in postgres
	id = db.Column(db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime)
	message = db.Column(db.String(200)) #message posted
	user_name = db.Column(db.String(80))#, ForeignKey("logappuser.username")) #the user who posted the message
	messagejson = db.Column(JSON)

	def __init__(self, datetime, message, username):
		self.datetime = datetime
		self.message = message
		self.user_name = username

db.create_all() #creating the databases

@app.route("/", methods =['POST', 'GET'])  #changing view after a message is posted
def index():  #name of the url to put in url_for in html
    if request.method == "GET": 
    	datevar = request.args.get('date') #use args.get for HTTP GET methods
        if datevar:
            dateobject = datetime.strptime(datevar, '%Y-%m-%d') #change the string to Python date object
            max_time = datetime.combine(dateobject, time.max) 
            return render_template("index.html", filtered_data = Logmessage.query.order_by(desc(Logmessage.datetime)).filter(Logmessage.datetime <= max_time, Logmessage.datetime >= dateobject).all())
        else:
        	return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all())

    elif request.method == "POST":
    	msgtext = request.form.get('messagebox') #use form.get for HTTP POST methods
        if msgtext:
            current_datetime = datetime.now(timezone("Indian/Maldives"))  #take time to be GMT+5
            data = Logmessage(current_datetime, msgtext, "nazaal") #must change username, taking it from external server
            db.session.add(data)
            db.session.commit()
            return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all()) 
        else:
   	        return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all()) 
    else:
        return render_template("index.html", messagelist = Logmessage.query.order_by(desc(Logmessage.datetime)).all()) #casting to make types match

if __name__ == "__main__":
	app.debug = True
	app.run(host = "0.0.0.0")