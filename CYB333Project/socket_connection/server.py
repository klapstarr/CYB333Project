
import socket

HOST = "127.0.0.1"
PORT = 50000
BUFFER_SIZE = 1024


def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)

            print(f"[SERVER] Listening on {HOST}:{PORT}")
            print("[SERVER] Waiting for client connection...")

            conn, address = server.accept()

            with conn:
                print(f"[SERVER] Connected by {address}")

                while True:
                    data = conn.recv(BUFFER_SIZE)

                    if not data:
                        print("[SERVER] Client disconnected.")
                        break

                    message = data.decode("utf-8")
                    print(f"[CLIENT] {message}")

                    if message.lower() == "quit":
                        response = "Goodbye!"
                        conn.sendall(response.encode("utf-8"))
                        print("[SERVER] Closing connection.")
                        break

                    response = f"Server received: {message}"
                    conn.sendall(response.encode("utf-8"))

    except OSError as error:
        print(f"[SERVER ERROR] {error}")

    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped.")

    finally:
        print("[SERVER] Shutdown complete.")


if __name__ == "__main__":
    start_server()

