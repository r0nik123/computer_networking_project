import subprocess
import time
import os


def run_simulation():
    # Get the absolute path of the current directory to locate server and client scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("--- Starting Chat System Simulation ---")

    # Launch the Server
    print("[SIMULATION] Launching Chat Server...")
    subprocess.Popen(
        [
            "osascript",
            "-e",
            f'tell app "Terminal" to do script "python3 {current_dir}/server.py"',
        ]
    )

    # Wait for the server to initialize and start listening on the port
    time.sleep(2)

    # List of clients to launch automatically
    clients = ["Yossi", "Dana", "Roni"]

    # Launch each client in a separate Terminal window
    for name in clients:
        print(f"[SIMULATION] Launching Client Instance: {name}...")
        subprocess.Popen(
            [
                "osascript",
                "-e",
                f'tell app "Terminal" to do script "python3 {current_dir}/client.py {name}"',
            ]
        )
        # Brief pause to ensure orderly connection to the server
        time.sleep(1)

    print("\n[SUCCESS] Simulation is running.")
    print("Instructions: Use the opened Terminal windows to communicate.")
    print("Format: 'RecipientName:YourMessage' (e.g., 'Dana:Hello')")


if __name__ == "__main__":
    run_simulation()
