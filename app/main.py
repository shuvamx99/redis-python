# Uncomment this to pass the first stage
import socket
import threading

db = {}

def set(key, value):
    db[key] = value
    return "+OK\r\n"

def get(key):
    value = db[key]
    length = len(value)
    return f"${length}\r\n{value}\r\n"

def handle_client(client_socket):
    with client_socket:
        while True:
            recv = client_socket.recv(1024)
            if not recv:
                break
            command = parse_redis_command(recv.decode())
            print(f"command : {command}")

            if command:
                response = execute_command(command)
                client_socket.sendall(response.encode())

def execute_command(command):

    if command[0].upper() == "PING":
        return "+PONG\r\n"
    elif command[0].upper() == "ECHO":
        return f"+{command[1]}\r\n"
    elif command[0].upper() == "SET":
        return set(command[1], command[2])
    elif command[0].upper() == "GET":
        return get(command[1])
    else:
        return "-ERR\r\n"

def parse_redis_command(command_str):
    parts = command_str.strip().split("\r\n")
    # Extracting the number of arguments
    num_args = int(parts[0][1:])
    # Extracting the arguments
    args = []
    i = 1
    while i < len(parts):
        arg_length = int(parts[i][1:])
        arg = parts[i + 1][:arg_length]
        args.append(arg)
        i += 2
    return args

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
