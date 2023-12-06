echo "Response:"
curl --header "Content-Type: application/json" --request POST --data '{"First Name":"Alice", "Last Name":"Doe", "Email Address":"alice.doe@peoplesuite.com", "Country": "US"}' http://localhost:8080/
#curl http://localhost:8080/employees
#for GET a list of all employees