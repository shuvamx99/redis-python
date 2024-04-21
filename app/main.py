# Uncomment this to pass the first stage
import socket
import threading

def handle_client(client_socket):
    with client_socket:
        while True:
            recv = client_socket.recv(1024)
            if not recv:
                break
            client_socket.sendall("+PONG\r\n".encode())
    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    print("Server is waiting for Client to connect ...")
    
    while True:
        client_socket, addr = server_socket.accept() # wait for client
        print(f"Connection made with {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
