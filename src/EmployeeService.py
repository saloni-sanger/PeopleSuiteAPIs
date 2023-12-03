from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
"""
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://mysql:3308' 
# mysql protocol to server at mysql (service name), will ask k8 DNS for IP of mysql (the service), then connect to IP it gets back on port 3308 (our service's IP port)

db = SQLAlchemy(app) #db is a client instance configured from the mysql service
class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))

def __init__(self, name, city, addr,pin): #creating an object for students table
   self.name = name
   self.city = city
   self.addr = addr
   self.pin = pin

db.create_all()
"""
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#i have code to build a docker image (Dockerfile)
#to run in k8, 
#k8 is gonna run the image the Dockerfile makes
#k8 will use a yaml deployment