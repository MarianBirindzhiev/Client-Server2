import socket

# Constants for communication
HEADER = 64
PORT = 5000
SERVER = "192.168.100.57"  # Server IP address
#SERVER = socket.gethostbyname(socket.gethostname())  # Use local hostname to automatically get server IP
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create a socket object and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Function to handle receiving messages from the server
def handle_server():
    # Receive the message length from the server
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        # If message length is received, decode it and receive the message
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        # Print the sorted array received from the server
        print(f"[SERVER] The sorted array is: {msg}")

# Function to get input from the user and send it to the server
def get_input():
    # Prompt the user to input an array to be sorted
    user_input = input("[INFORMATION] Send the array that you want to be sorted!: ")
    # Convert the input string to a list of integers
    user_input = list(map(int, user_input.split()))
    # Convert the list of integers back to a string with space-separated values
    user_input = ' '.join(map(str, user_input))
    # Send the input array to the server
    send(user_input)

# Function to send messages to the server
def send(msg):
    # Encode the message to bytes
    message = msg.encode(FORMAT)
    msg_length = len(message)
    # Encode the message length and pad it to the fixed header size
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # Send the message length followed by the message to the server
    client.send(send_length)
    client.send(message)
    # Handle any response from the server
    handle_server()

# Main logic
input("[INFORMATION] Press Enter to start!")
while True:
    # Get input from the user and send it to the server
    get_input()
    # Ask the user if they want to sort another array
    user_input = input("[INFORMATION] Do you want to sort another array? (yes/no): ")
    if user_input.lower() == "no":
        break

# Disconnect from the server
input("[INFORMATION] Press Enter to disconnect from the server!")
send(DISCONNECT_MESSAGE)
