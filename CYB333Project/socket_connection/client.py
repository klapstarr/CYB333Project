
import socket

HOST = "127.0.0.1"
PORT = 50000
BUFFER_SIZE = 1024


def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            print(f"[CLIENT] Connecting to {HOST}:{PORT}...")

            client.settimeout(5)
            client.connect((HOST, PORT))
            client.settimeout(None)

            print("[CLIENT] Connected successfully!")
            print("Type a message or 'quit' to disconnect.")

            while True:
                message = input("You: ")

                client.sendall(message.encode("utf-8"))

                response = client.recv(BUFFER_SIZE)

                if not response:
                    print("[CLIENT] Server disconnected.")
                    break

                print(f"[SERVER] {response.decode('utf-8')}")

                if message.lower() == "quit":
                    break

    except ConnectionRefusedError:
        print("[CLIENT ERROR] Server is not running.")

    except socket.timeout:
        print("[CLIENT ERROR] Connection timed out.")

    except OSError as error:
        print(f"[CLIENT ERROR] {error}")

    finally:
        print("[CLIENT] Disconnected.")


if __name__ == "__main__":
    start_client()
