from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from iso3166 import countries
import os

app = Flask(__name__)

#mysql protocol, mysql service on port 3306
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@mysql:3306/peoplesuite'.format(os.environ.get('DB_USER'), os.environ.get('DB_PASS')) 

#db is a client instance configured from the mysql service
db = SQLAlchemy(app) 

#Employee class will inherit db.Model's methods (db.Model is parent class, Employee is child class)
class Employee(db.Model): 
   __tablename__ = "Employees"
   id = db.Column('employee_id', db.Integer, primary_key = True)
   first = db.Column('first_name', db.String(50))
   last = db.Column('last_name', db.String(50))
   email = db.Column('email_address', db.String(100))  
   country = db.Column('country', db.String(2))

   def __init__(self, first, last, email, country): 
      self.first = first
      self.last = last
      self.email = email
      self.country = country

with app.app_context():
   db.create_all()

#test directory
@app.route('/employees/health')
def emp_health():
   return "healthy"

#specifying methods means other requests get ignored
@app.route('/employees', methods = ['GET', 'POST']) 
def table():
   if request.method == 'GET' :
      result = []
      EMPLOYEES = db.session.query(Employee).all()
      for employee in EMPLOYEES :
         #ordering is not insertion order (aplhabertical)
         emp = dict( 
            EmployeeID = employee.id,
            FirstName = employee.first,
            LastName = employee.last,
            EmailAddress = employee.email,
            Country = employee.country,
         )
         result.append(emp)
      #OK, request has succeeded
      return result, 200 
   #use the json sent in create Employee object and put it in the DB
   if request.method == 'POST' :
      #parse json to get Employee information
      if not request.is_json :
         #request is not json, send bad request error
         return 'request body must contain JSON', 400 

      #parses incoming JSON request data and returns it as a python dictionary
      content = request.get_json() 
      #check if country is in ISO-3166 library
      if countries.get(content['Country']) == None :
         #bad request
         return 'Country code must be in ISO-3166 format', 400 
      
      first, last, email, country = content['First Name'], content['Last Name'], content['Email Address'], content['Country']
      emp = Employee(first, last, email, country)
      #add() does not take what __init__ takes, it takes an instance of a class extending db.Model
      #it will 'ask' the object its type and fields and figure out what to do
      db.session.add(emp)
      db.session.commit()
      #no duplication control/avoidance
      created_object = Employee.query.filter_by(first = first, last = last, email = email, country = country).first() 
      if created_object is None :
         #internal server error
         return 'Failed to create object', 500 
      #ordering is not insertion order (alphabertical)
      result = dict( 
         EmployeeID = created_object.id,
         FirstName = created_object.first,
         LastName = created_object.last,
         EmailAddress = created_object.email,
         Country = created_object.country
      )
      #If you return a Python dictionary in a Flask view, the dictionary will automatically be converted to the JSON format for the response. (sentry.io)
      #successful creation
      return result, 201 

@app.route('/employees/<employee_id>', methods = ['GET'])
def get(employee_id):
   emp = db.session.query(Employee).filter(Employee.id==employee_id).first()
   if emp is None :
      #The requested resource was not found
      return "Employee ID doesn't exist", 404 
   return dict(
         EmployeeID = emp.id,
         FirstName = emp.first,
         LastName = emp.last,
         EmailAddress = emp.email,
         Country = emp.country,
   ), 200 #successful get