from flask import Flask, request
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection 
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine.models import Model
from iso3166 import countries

app = Flask(__name__)

app.config['CASSANDRA_SETUP_KWARGS'] = {'port': 9042}
connection.setup(['cassandra'], "cqlengine", protocol_version=3) #try 127.0.0.1 instead of cass, is localhost
create_keyspace_simple('cqlengine', 1)

#constructed using flask app so it can 'deeply integrate' with it
class Employee(Model): #employee class will inherit db.Model's methods (db.Model is parent class, employee is child class)
   __tablename__ = "Employees"
   id = columns.UUID(primary_key = True, default=uuid.uuid4)
   first = columns.Text(index = True)
   last = columns.Text(index = True)
   email = columns.Text(index = True)  
   country = columns.Text(index = True)
   # run validation on country code to make sure it's one of them (use library) when you get a POST, send error code if not

sync_table(Employee)

@app.route('/employees/deleteall')
def delete():
   EMPLOYEES = Employee.objects()
   for employee in EMPLOYEES :
        Employee.delete(employee)
   return "deleted", 200

@app.route('/employees', methods = ['GET', 'POST']) #specifying methods means other requests get ignored
def table():
   if request.method == 'GET' :
      result = []
      EMPLOYEES = Employee.objects()
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
      #create() inserts into the table too, returns the instance created (no clear error return tho, so double check)
      emp = Employee.create(first = first, last = last, email = email, country = country)
      try:
         created_object = Employee.get(id = emp.id)
      except:
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
   try: 
      emp = Employee.get(id = employee_id)
   except:
      return "Employee ID doesn't exist", 404 #The requested resource was not found
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