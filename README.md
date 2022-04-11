Description
===========

Real time chat implemented on asynchronous TCP server

server:

• accepts requests from clients;

• supports multiple clients at the same time;

• delivers the message to the addressee;

• informs the sender about success or failure;

• logs client messages to syslog.


clients:

• receive messages from the server;

• send messages;

• receive a delivery confirmation.

the client works in two threads, first for reading, second for writing to the server


Installation
============


python3 setup.py sdist

virtualenv env

source ./env/bin/activate

./env/bin/python3 setup.py install



Start
=====
source ./env/bin/activate



Commands
========

runserver

runclient

