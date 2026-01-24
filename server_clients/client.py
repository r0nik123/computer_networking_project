import socket
import threading
import sys


class ChatClient:
    def __init__(self, name):
        self.name = name
        # Create a TCP/IP socket using IPv4
        # socket.AF_INET specifies IPv4 address family
        # socket.SOCK_STREAM specifies TCP protocol
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 8888

    def receive_messages(self):
        """
        Background thread to handle incoming messages from the server.
        """
        while True:
            try:
                # Receive and decode data from the server
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    # Format the incoming message for better visibility
                    # ensures it starts on a new line, [RECEIVE] marks it as incoming
                    print(f"\n\n[RECEIVE] {message}")
                    # Re-print the input prompt so the user knows they can still type
                    print("Send [Target:Message] or 'quit': ", end="", flush=True)
            except:
                # If the connection fails, notify the user and exit the thread
                print("\n[SYSTEM] Connection to server lost.")
                break

    def start(self):
        """
        Initializes the TCP connection and starts the main chat loop.
        """
        try:
            # Connect the socket to the server's address and port using Three-Way Handshake
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"[ERROR] Could not connect to server: {e}")
            return

        # Send the username to the server immediately after connecting
        self.client_socket.send(self.name.encode("utf-8"))

        # Start a background thread to listen for incoming messages from the server
        # This allows the client to receive data while waiting for user input
        # daemon=True ensures the thread exits when the main program is closed
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        print(f"--- Welcome to the chat, {self.name}! ---")

        # Main loop: get user input and send it to the server.
        # If "quit" is entered, break the loop and close the connection.
        while True:
            # Display an intuitive input prompt
            msg = input("Send [Target:Message] or 'quit': ")

            if msg.lower() == "quit":
                print("[SYSTEM] Closing connection...")
                break

            try:
                # Send encoded data to the server
                self.client_socket.send(msg.encode("utf-8"))
            except BrokenPipeError:
                print("[ERROR] Server is unreachable.")
                break

        # Gracefully close the socket connection
        self.client_socket.close()


if __name__ == "__main__":
    # Check if a username was passed as a command-line argument (used by simulation script)
    if len(sys.argv) > 1:
        # sys.argv[1] contains the first parameter after the filename
        my_name = sys.argv[1]
    else:
        # If no argument was provided, prompt the user for manual input
        my_name = input("Enter your name: ")

    # Create an instance of ChatClient and launch the connection process
    client = ChatClient(my_name)
    client.start()
