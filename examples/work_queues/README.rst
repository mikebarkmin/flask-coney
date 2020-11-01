Hello World
===========

Start the services::

  $ docker-compose up

Send a request to service1::

  $ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"Hi":"Ho"}' \
  http://localhost:5001/process

Check the processed request on service2::

  $ docker-compose logs service2
