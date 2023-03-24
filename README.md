# api-test

# test in dev: 
docker-compose up 
# examples
curl -X PUT http://localhost:8181/api/hello/danilo -H 'Authorization: Bearer fake-token' -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"dateOfBirth": "1986-09-15"}'
curl -X GET -H 'Authorization: Bearer fake-token' http://localhost:8181/api/hello/danilo
# api documentation
http://localhost:8181/docs