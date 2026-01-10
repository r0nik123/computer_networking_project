import socket
import threading


def handle_client(client_socket, address, clients):
    """
    Handles communication with a single client in a separate thread.
    """
    username = ""
    try:
        # Step A: Receive the username from the client immediately upon connection
        username = client_socket.recv(1024).decode("utf-8").strip()

        # Register the client in the shared dictionary for message routing
        clients[username] = client_socket
        print(f"[SERVER] {username} connected from {address}")

        while True:
            # Step B: Wait for an incoming message in the format "Target:Message"
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                # If no data is received, the client likely disconnected
                break

            if ":" in data:
                # Split the data into the target recipient and the actual message
                target, msg = data.split(":", 1)

                if target in clients:
                    # Route the message to the target client's specific socket
                    clients[target].send(f"[{username}]: {msg}".encode("utf-8"))
                else:
                    # Notify the sender that the target user is unavailable
                    client_socket.send(
                        f"System: User '{target}' is not online.".encode("utf-8")
                    )
    except:
        # Ignore errors and proceed to the finally block for cleanup
        pass
    finally:
        # Cleanup: Remove the user from the active clients dictionary and close the socket
        if username in clients:
            print(f"[SERVER] {username} disconnected.")
            del clients[username]
        client_socket.close()


def start_server():
    # Initialize a TCP/IP socket using IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the local address and port 8888
    server.bind(("127.0.0.1", 8888))

    # Listen for incoming connections (allow a backlog of up to 5)
    server.listen(5)

    # A dictionary to manage active clients: {username: socket_object}
    clients = {}
    print("[SERVER] Listening on port 8888...")

    while True:
        # Accept a new incoming connection (Blocks until a client connects)
        conn, addr = server.accept()

        # Spawn a new thread to handle this specific client concurrently
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.start()


if __name__ == "__main__":
    start_server()
