from flask import Flask, send_from_directory, request, current_app
from sqlalchemy import Table, Column, Integer, DateTime, desc
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from datetime import datetime, time
from pytz import timezone

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/logappdb'
db = SQLAlchemy(app)

class Logmessage(db.Model):   #database model class
	__tablename__ = "logmessages"  #table name in postgres
	id = db.Column(db.Integer, primary_key = True)
	datetime = db.Column(db.DateTime)
	message = db.Column(db.String(200))
	user_name = db.Column(db.String(80))

	def __init__(self, datetime, message, username):
		self.datetime = datetime
		self.message = message
		self.user_name = username

db.create_all() #creating the databases, needs to happen once 

class MessagesList(Resource):
    def get(self):  #returns all messages in JSON format
        querydata = Logmessage.query.order_by(desc(Logmessage.datetime))
        jsondata = [{'date': msg.datetime.strftime("%Y-%m-%d"), 'username': msg.user_name,  'time': msg.datetime.strftime("%H:%M:%S"), 'message': msg.message} for msg in querydata]
        datefield = request.args.get('date')  #gets the date form the user
        if datefield:
            dateobject = datetime.strptime(datefield, '%Y-%m-%d') #change the string to Python date object
            max_time = datetime.combine(dateobject, time.max)
            filteredquery = querydata.filter(Logmessage.datetime >= dateobject).filter(Logmessage.datetime <= max_time)  #combining both queries with and results in a boolean value error
            return [{'date': msg.datetime.strftime("%Y-%m-%d"), 'username': msg.user_name,  'time': msg.datetime.strftime("%H:%M:%S"), 'message': msg.message} for msg in filteredquery]
        else:
            return jsondata
    
class Message(Resource):    
    def post(self):
        parser = reqparse.RequestParser() #we need to parse what we get from AngularJS
        parser.add_argument('message', type=str, help='Event logged by user')
        args = parser.parse_args()
        msgtext = args['message']  #this is the message used in postman key value
        if msgtext:
            current_datetime = datetime.now(timezone("Indian/Maldives"))  #take time to be GMT+5
            username = "Nazaal"
            data = Logmessage(current_datetime, msgtext, username)
            db.session.add(data)
            db.session.commit()
            return {'date': current_datetime.strftime("%Y-%m-%d"), 'username': username, 'time': current_datetime.strftime("%H:%M:%S"), 'message': msgtext}, 201

# class Search(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('date', type=str, help='Date to search')
#         args = parser.parse_args()
#         searchdate = args['date']
#         if searchdate:
#             dateobject = datetime.strptime(searchdate, '%Y-%m-%d') #change the string to Python date object
#             max_time = datetime.combine(dateobject, time.max)
#             json_search = [{'date' : msg.datetime.strftime("%Y-%m-%d"), 'username': msg.user_name,  'time': msg.datetime.strftime("%H:%M:%S"), 'message': msg.message} for msg in Logmessage.query.all().filter(Logmessage.datetime >= dateobject and Logmessage.datetime <= max_time)]
#             return json_search

api.add_resource(MessagesList, '/messages') #creates API to show messages, using ?date=2017-09-12 to search by date
api.add_resource(Message, '/messages') #creates API to post messages
# api.add_resource(Search, '/messages/search') #search API

# @app.route("/", methods =['POST', 'GET'])  #changing view after a message is posted/searched
# def index():  #name of the url to put in url_for in html
#     dbobject = Logmessage.query.order_by(desc(Logmessage.datetime))  #loads all logs and sorts them in descending order of time
#     if request.method == "POST": 
#         datevar = request.args.get('date') #use args.get for HTTP GET methods
#         if datevar:
#             dateobject = datetime.strptime(datevar, '%Y-%m-%d') #change the string to Python date object
#             max_time = datetime.combine(dateobject, time.max) 
#             json_search = [{'date' : msg.datetime.strftime("%Y-%m-%d"), 'username': msg.user_name,  'time': msg.datetime.strftime("%H:%M:%S"), 'message': msg.message} for msg in Logmessage.query.filter(Logmessage.datetime >= dateobject and Logmessage.datetime <= max_time)]
#             return send_from_directory('/var/www/logapp/templates/',"index.html")  #method send_from_directory for AngularJS templates, render_template for Jinja templates
#         else:
#         	return send_from_directory('/var/www/logapp/templates/',"index.html")
#     else:
#     	msgtext = request.form.get('messagebox') #use form.get for HTTP POST methods
#         if msgtext:
#             current_datetime = datetime.now(timezone("Indian/Maldives"))  #take time to be GMT+5
#             data = Logmessage(current_datetime, msgtext, "nazaal") #must change username, taking it from external server
#             db.session.add(data)
#             db.session.commit()
#             return send_from_directory('/var/www/logapp/templates/',"index.html") 
#         # else:
#    	    #     return send_from_directory('/var/www/logapp/templates/',"index.html") 
#     return send_from_directory('/var/www/logapp/templates/',"index.html") 

if __name__ == "__main__":
	app.debug = True
	app.run(host = "0.0.0.0")