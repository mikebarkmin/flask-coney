Routing
=======

Start the services::

  $ docker-compose up

Send a request to service1::

  $ curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5001/warning

  $ curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5001/error

  $ curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5001/info

Check the processed request on service2 and service3::

  $ docker-compose logs service2 service3
