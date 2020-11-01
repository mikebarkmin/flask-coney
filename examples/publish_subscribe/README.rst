Publish Subscribe
=================

Start the services::

  $ docker-compose up

Send a request to service1 and service2::

  $ curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5001/pub

Check the processed request on service1 and service2::

  $ docker-compose logs service1 service2
