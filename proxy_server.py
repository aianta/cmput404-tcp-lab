import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request):
    # Send request
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host,port))
        client_socket.send(request)
        
        # Assemble response 
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while(b"</html>" not in result):
            data = client_socket.recv(BYTES_TO_READ)
            result += data
    
        # Return response
        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            response = send_request("www.google.com", 80, data)
            conn.sendall(response)
        

# Start single-threaded proxy server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) #Allow queuing of up to 2 connections
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

# Start multi-threaded proxy server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST,PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # Allow queuing of up to 2 connections
        
        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()



#start_server()
start_threaded_server()

'''
See which ports are active: 
lsof -nP | grep LISTEN

Kill processes, in increasing order of danger:
pkill python

sudo kill <pid>

sudo kill -9 <pid>

'''