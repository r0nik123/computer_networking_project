import socket
import threading
import sys


def receive_messages(sock):
    """
    Background thread to handle incoming messages from the server.
    """
    while True:
        try:
            # Receive and decode data from the server
            message = sock.recv(1024).decode("utf-8")
            if message:
                # Format the incoming message for better visibility
                # \n ensures it starts on a new line, >>> marks it as incoming
                print(f"\n\n[RECEIVE] {message}")
                # Re-print the input prompt so the user knows they can still type
                print("Send [Target:Message] or 'quit': ", end="", flush=True)
        except:
            # If the connection fails, notify the user and exit the thread
            print("\n[SYSTEM] Connection to server lost.")
            break


def start_client(name):
    # Create a TCP/IP socket using IPv4
    # socket.AF_INET means use IPv4
    # socket.SOCK_STREAM means using TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect the socket to the server's address and port using three way shaking hands
        client.connect(("127.0.0.1", 8888))
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return

    # Send the username to the server immediately after connecting
    client.send(name.encode("utf-8"))

    # Start a background thread to listen for incoming messages from the server
    # This allows the client to receive data while waiting for user input
    # daemon=True ensures the thread exits when the main program is closed
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    print(f"--- Welcome to the chat, {name}! ---")
    # If "quit" is entered, break the loop and close the connection.
    while True:
        # Display an intuitive input prompt
        msg = input("Send [Target:Message] or 'quit': ")

        if msg.lower() == "quit":
            print("[SYSTEM] Closing connection...")
            break

        # Send encoded data to the server
        client.send(msg.encode("utf-8"))
    client.close()


if __name__ == "__main__":
    # Check if a username was passed as a command-line argument
    if len(sys.argv) > 1:
        # sys.argv[1] contains the first parameter after the filename
        my_name = sys.argv[1]
    else:
        # If no argument was provided, prompt the user for manual input
        my_name = input("Enter your name: ")
    # Launch the client connection process with the determined username
    start_client(my_name)
