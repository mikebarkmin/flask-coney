Request Reply
=============

Start the services::

  $ docker-compose up

Send a request to service1::

  $ curl --header "Content-Type: application/json" \
  --request GET \
  http://localhost:5001/rpc
