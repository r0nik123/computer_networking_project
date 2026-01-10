import socket
import threading


class ChatServer:
    def __init__(self, host="127.0.0.1", port=8888):
        # Initialize a TCP/IP socket using IPv4
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow immediate reuse of the port after server restart
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the local address and port
        self.server.bind((host, port))

        # A dictionary to manage active clients: {username: socket_object}
        self.clients = {}
        self.host = host
        self.port = port

    def handle_client(self, client_socket, address):
        """
        Handles communication with a single client in a separate thread.
        """
        username = ""
        try:
            # Step A: Receive the username from the client immediately upon connection
            username = client_socket.recv(1024).decode("utf-8").strip()

            # Register the client in the shared dictionary for message routing
            self.clients[username] = client_socket
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

                    if target in self.clients:
                        # Route the message to the target client's specific socket
                        self.clients[target].send(
                            f"[{username}]: {msg}".encode("utf-8")
                        )
                    else:
                        # Notify the sender that the target user is unavailable
                        client_socket.send(
                            f"System: User '{target}' is not online.".encode("utf-8")
                        )
        except (ConnectionResetError, BrokenPipeError):
            # Specific error handling for unexpected disconnections
            print(f"[ERROR] Unexpected disconnect from {username}")
        except Exception as e:
            # Catch other potential errors
            print(f"[ERROR] Error handling client {username}: {e}")
        finally:
            # Cleanup: Remove the user from the active clients dictionary and close the socket
            if username in self.clients:
                print(f"[SERVER] {username} disconnected.")
                del self.clients[username]
            client_socket.close()

    def start(self):
        # Listen for incoming connections (allow a backlog of up to 5)
        self.server.listen(5)
        print(f"[SERVER] Listening on {self.host}:{self.port}...")

        while True:
            # Accept a new incoming connection (Blocks until a client connects)
            conn, addr = self.server.accept()

            # Spawn a new thread to handle this specific client concurrently
            # We pass 'self.handle_client' because it's now a method of the class
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    # Create an instance of the ChatServer class
    chat_server = ChatServer()
    # Start the server
    chat_server.start()
