from flask import Flask, request
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection 
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine.models import Model
from iso3166 import countries

app = Flask(__name__)

app.config['CASSANDRA_SETUP_KWARGS'] = {'port': 9042}
connection.setup(['cassandra'], "cqlengine", protocol_version=3)
create_keyspace_simple('cqlengine', 1)

class Employee(Model):
   __tablename__ = "Employees"
   id = columns.UUID(primary_key = True, default=uuid.uuid4)
   first = columns.Text(index = True)
   last = columns.Text(index = True)
   email = columns.Text(index = True)  
   country = columns.Text(index = True)

sync_table(Employee)

@app.route('/employees/deleteall')
def delete():
   EMPLOYEES = Employee.objects()
   for employee in EMPLOYEES :
        Employee.delete(employee)
   return "deleted", 200

#specifying methods means other requests get ignored
@app.route('/employees', methods = ['GET', 'POST']) 
def table():
   if request.method == 'GET' :
      result = []
      EMPLOYEES = Employee.objects()
      for employee in EMPLOYEES :
         #ordering is not insertion order (it's alphabetical)
         emp = dict( 
            EmployeeID = employee.id,
            FirstName = employee.first,
            LastName = employee.last,
            EmailAddress = employee.email,
            Country = employee.country,
         )
         result.append(emp)
      #OK, request has succeeded
      #return a list of dictionaries and flask will convert output to JSON
      return result, 200 
   #use the json sent in to create Employee object and put it in the DB
   if request.method == 'POST' :
      #parse json to add employee to the table
      if not request.is_json :
         #request is not json, send bad request error
         return 'request body must contain JSON', 400 
      
      #parses incoming JSON request data and returns the data as a python dictionary
      content = request.get_json() 
      #check if country is in ISO-3166 library
      if countries.get(content['Country']) == None :
         #request is bad
         return 'Country code must be in ISO-3166 format', 400 
      
      first, last, email, country = content['First Name'], content['Last Name'], content['Email Address'], content['Country']
      #create() inserts into the table too, returns the instance created (no clear error return tho, so double check insertion)
      emp = Employee.create(first = first, last = last, email = email, country = country)
      try:
         created_object = Employee.get(id = emp.id)
      except:
         #internal server error
         return 'Failed to create object', 500 
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
   try: 
      emp = Employee.get(id = employee_id)
   except:
      #The requested resource was not found
      return "Employee ID doesn't exist", 404 
   return dict(
         EmployeeID = emp.id,
         FirstName = emp.first,
         LastName = emp.last,
         EmailAddress = emp.email,
         Country = emp.country,
   ), 200 #successful get
