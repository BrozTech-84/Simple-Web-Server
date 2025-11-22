# Simple web server (python sockets)

This project is a group assignment to build a simple web server from scratch using python sockets.
The goal is to understand how HTTP works under the hood.

## Project structure
 - 'server/' -> python server code
 - 'static/' -> HTML/CSS/images served by the server
 - 'tests/' -> Unit tests
 - 'docs/' -> Design & documentation
 - 'examples/' -> Demo scripts and sample requests

 ## How to Run 
  1. Basic TCP Socket Server 

   (a.) Bind to a Port
The server attaches itself to a specific IP + port (e.g., 127.0.0.1:8080) so browsers can find it.
 
    (b.) Listen for Connections 
After binding, the server enters a listening state, waiting for incoming client requests.
   
    (c.) Accept Client Connections
 When a browser attempts to connect, the server accepts the connection and establishes communication.
   
    (d.) Receive and Print Raw HTTP Requests 
The server receives the full HTTP request message sent by the browser and prints it out to the terminal.


  2. 


