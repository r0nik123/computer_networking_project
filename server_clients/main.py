import subprocess
import time
import os


def run_simulation():
    # Get the path of the current directory to ensure scripts are found
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Starting Server...")
    # Launch server.py in a new Terminal window using AppleScript (macOS)
    subprocess.Popen(
        [
            "osascript",
            "-e",
            f'tell app "Terminal" to do script "python3 {current_dir}/server.py"',
        ]
    )
    # Pause to allow the server to initialize and start listening for connections
    time.sleep(2)

    print("Starting Client: Yossi...")
    # Launch a client instance for 'Yossi' in a new Terminal window
    subprocess.Popen(
        [
            "osascript",
            "-e",
            f'tell app "Terminal" to do script "python3 {current_dir}/client.py Yossi"',
        ]
    )
    # Brief pause between client launches to prevent connection collisions
    time.sleep(1)

    print("Starting Client: Dana...")
    # Launch a client instance for 'dana' in a new Terminal window
    subprocess.Popen(
        [
            "osascript",
            "-e",
            f'tell app "Terminal" to do script "python3 {current_dir}/client.py Dana"',
        ]
    )

    print("\nSimulation running. Use the separate Terminal windows to chat!")
    print("Example: In Yossi's window type 'Dana:Hello from Yossi'")


if __name__ == "__main__":
    run_simulation()
