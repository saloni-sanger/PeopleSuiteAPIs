from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from iso3166 import countries
import os

app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@mysql:3306/peoplesuite'.format(os.environ.get('DB_USER'), os.environ.get('DB_PASS')) 
#mysql protocol, mysql service on port 3306
# mysql protocol to server at mysql (service name), will ask k8 DNS for IP of mysql (the service), then connect to IP it gets back on port 3308 (our service's IP port)

db = SQLAlchemy(app) #db is a client instance configured from the mysql service
#constructed using flask app so it can 'deeply integrate' with it
class Employee(db.Model): #employee class will inherit db.Model's methods (db.Model is parent class, employee is child class)
   __tablename__ = "Employees"
   id = db.Column('employee_id', db.Integer, primary_key = True)
   first = db.Column('first_name', db.String(50))
   last = db.Column('last_name', db.String(50))
   email = db.Column('email_address', db.String(100))  
   country = db.Column('country', db.String(2))
   # run validation on country code to make sure it's one of them (use library) when you get a POST, send error code if not

   def __init__(self, first, last, email, country): #constructor for SQLAlchemy or me, used for add
      self.first = first
      self.last = last
      self.email = email
      self.country = country

with app.app_context():
   db.create_all()

@app.route('/employees/health')
def emp_health():
   return "healthy"

@app.route('/employees', methods = ['GET', 'POST']) #specifying methods means other requests get ignored
def table():
   if request.method == 'GET' :
      result = []
      EMPLOYEES = db.session.query(Employee).all()
      #query = SQLAlchemy.select('Employees')
      #EMPLOYEES = db.execute(query).fetchall()
      for employee in EMPLOYEES :
         emp = dict( #ordering is not insertion order (aplhabertical)
            EmployeeID = employee.id,
            FirstName = employee.first,
            LastName = employee.last,
            EmailAddress = employee.email,
            Country = employee.country,
         )
         result.append(emp)
      return result, 200 #OK, request has succeeded
      #return list of each employee information in JSON
      #return list of dictionaries
   if request.method == 'POST' :
      #parse json to add employee to the table
      #use the json sent in create object and put it in db
      if not request.is_json :
         return 'request body must contain JSON', 400 #request is not json, send bad request error

      content = request.get_json() #parses incoming JSON request data and returns i8t as a python dictionary
      if countries.get(content['Country']) == None :#check if country is in ISO-3166 library
         return 'Country code must be in ISO-3166 format', 400 #request is bad
      
      first, last, email, country = content['First Name'], content['Last Name'], content['Email Address'], content['Country']
      emp = Employee(first, last, email, country)
      db.session.add(emp)#add does not take what __init__ takes, it takes an instance of a class extending db.Model
      #it will 'ask' the object its type and fields and figure out what to do
      db.session.commit()
      created_object = Employee.query.filter_by(first = first, last = last, email = email, country = country).first() #no gaurantee it's the same obj, no duplication control/avoidance
      #print(created_object) #test
      if created_object is None :
         return 'Failed to create object', 500 #internal server error
      result = dict( #ordering is not insertion order (aplhabertical)
         EmployeeID = created_object.id,
         FirstName = created_object.first,
         LastName = created_object.last,
         EmailAddress = created_object.email,
         Country = created_object.country
      )
      #If you return a Python dictionary in a Flask view, the dictionary will automatically be converted to the JSON format for the response. (sentry.io)
      return result, 201 #successful creation
      #create json to send back (say the content type is json)
      #return

@app.route('/employees/<employee_id>', methods = ['GET'])
def get(employee_id):
   emp = db.session.query(Employee).filter(Employee.id==employee_id).first()
   if emp is None :
      return "Employee ID doesn't exist", 400 #bad request
   return dict(
         EmployeeID = emp.id,
         FirstName = emp.first,
         LastName = emp.last,
         EmailAddress = emp.email,
         Country = emp.country,
   ), 200 #successful get
   #only one method, so do ur get here

#i have code to build a docker image (Dockerfile)
#to run in k8, 
#k8 is gonna run the image the Dockerfile makes
#k8 will use a yaml deployment