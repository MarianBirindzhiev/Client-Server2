# Client-Server

This project is a client-server application that uses sockets for communication. The server accepts connections from multiple clients and sorts arrays of numbers sent by the clients using a parallel version of the quicksort algorithm.

## Features

- Multithreaded server that can handle multiple client connections simultaneously.
- Efficient sorting of arrays using a parallel quicksort algorithm.
- Clean and modular code that's easy to understand and modify.

## Requirements

- Python 3.6 or higher

## Usage

1. Run the server script: `python server.py`
2. Run the client script in a separate terminal window: `python client.py`
3. Enter an array of numbers in the client script to have it sorted by the server.
