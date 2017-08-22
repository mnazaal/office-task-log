from flask import Flask, render_template, request
from sqlalchemy import Table, Column, Integer, DateTime, desc
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
import json
from datetime import datetime, time
from pytz import timezone


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mnazaal'
db = SQLAlchemy(app)

class Logmessage(db.Model):
	__tablename__ = "logmessages"  #table name in postgres
	id = db.Column(db.Integer, primary_key = True)
	datetime = db.Column(db.DateTime)
	message = db.Column(db.String(200))
	user_name = db.Column(db.String(80))

	def __init__(self, datetime, message, username):
		self.datetime = datetime
		self.message = message
		self.user_name = username

db.create_all() #creating the databases

class Messages(Resource):
	def get(self):  #returns all messages in JSON format
		return [{'username': msg.user_name, 'time': msg.datetime.strftime("%Y-%m-%d %H:%M:%S"), 'message': msg.message} for msg in Logmessage.query.all()]

api.add_resource(Messages, '/messages')

@app.route("/", methods =['POST', 'GET'])  #changing view after a message is posted/searched
def index():  #name of the url to put in url_for in html
    dbobject = Logmessage.query.order_by(desc(Logmessage.datetime))
    if request.method == "GET": 
    	datevar = request.args.get('date') #use args.get for HTTP GET methods
        if datevar:
            dateobject = datetime.strptime(datevar, '%Y-%m-%d') #change the string to Python date object
            max_time = datetime.combine(dateobject, time.max) 
            return render_template("index.html", messagelist = dbobject.filter(Logmessage.datetime <= max_time, Logmessage.datetime >= dateobject).all())
        else:
        	return render_template("index.html", messagelist = dbobject.all())
    else:
    	msgtext = request.form.get('messagebox') #use form.get for HTTP POST methods
        if msgtext:
            current_datetime = datetime.now(timezone("Indian/Maldives"))  #take time to be GMT+5
            data = Logmessage(current_datetime, msgtext, "nazaal") #must change username, taking it from external server
            db.session.add(data)
            db.session.commit()
            return render_template("index.html", messagelist = dbobject.all())
        else:
   	        return render_template("index.html", messagelist = dbobject.all())


if __name__ == "__main__":
	app.debug = True
	app.run(host = "0.0.0.0")