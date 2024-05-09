import socket
import threading
import concurrent.futures

# Constants for socket communication
HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())  # Get local IP address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address
server.bind(ADDR)

# Define the quicksort algorithm
def quick_sort(arr):
    # Base case: if the array has 0 or 1 elements, it is already sorted
    if len(arr) <= 1:
        return arr
    else:
        # Choose the first element as the pivot
        pivot = arr[0]
        # Partition the array into elements less than or equal to the pivot and elements greater than the pivot
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        # Use ThreadPoolExecutor to sort the partitions concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            less_future = executor.submit(quick_sort, less)
            greater_future = executor.submit(quick_sort, greater)
            # Merge the sorted partitions with the pivot
            return less_future.result() + [pivot] + greater_future.result()

# Function to send messages over the connection
def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    # Pad the message length to ensure it's HEADER bytes long
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # Send the message length followed by the message
    conn.send(send_length)
    conn.send(message)

# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        # Receive the message length from the client
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            # If a message length is received, decode it and receive the message
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                # If the message is the disconnect message, close the connection
                connected = False
                print(f"[DISCONNECTED] {addr} disconnected")
            else:
                try:
                    # Try to parse the received message as an integer array
                    arr = list(map(int, msg.split()))
                    # Sort the array using quicksort
                    sorted_arr = quick_sort(arr)
                    # Convert the sorted array to a string and send it back to the client
                    sorted_arr = ' '.join(map(str, sorted_arr))
                    send(conn, sorted_arr)
                except ValueError:
                    # If parsing fails, print an error message
                    print(f"[ERROR] {addr} sent an invalid array!: {msg}")

    # Close the connection when the loop exits
    conn.close()

# Function to start the server and handle incoming connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Accept incoming connections
        conn, addr = server.accept()
        # Create a new thread to handle each connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Entry point of the script
if __name__ == "__main__":
    print("[STARTING] Server is starting!")
    start()
