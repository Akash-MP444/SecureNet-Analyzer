import socket
import ssl
import threading
import json
import os

HOST = '0.0.0.0'
PORT = 5000

LOG_FILE = "logs/data.csv"

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Create CSV file with header if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("client_id,timestamp,speed\n")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    # Get client certificate info
    client_cert = conn.getpeercert()
    if client_cert:
        client_common_name = dict(x[0] for x in client_cert['subject'])['commonName']
        print(f"[CLIENT CERT] {client_common_name}")
    else:
        print("[CLIENT CERT] No certificate provided")
        conn.close()
        return

    try:
        data = conn.recv(1024)

        if not data:
            return

        try:
            msg = json.loads(data.decode())

            client_id = msg.get("client_id", "unknown")
            timestamp = msg.get("timestamp", "unknown")
            speed = msg.get("download_speed_mbps", 0)

            print(f"[DATA] {client_id} | {timestamp} | {speed} Mbps")

            # Save to CSV
            with open(LOG_FILE, "a") as f:
                f.write(f"{client_id},{timestamp},{speed}\n")

            conn.sendall("ACK".encode())

        except Exception as e:
            print("[JSON ERROR]", e)
            conn.sendall("ERROR".encode())

    except Exception as e:
        print("[CLIENT ERROR]", e)

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def start_server():
    # SSL setup with mutual authentication
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="certs/server_new.crt",
        keyfile="certs/server_new.key"
    )

    # Load CA certificate to verify client certificates
    context.load_verify_locations("certs/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED  # Require client certificates
    context.check_hostname = False

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[LISTENING] Server running on port {PORT}")

    # Wrap socket with SSL
    with context.wrap_socket(sock, server_side=True) as server:
        while True:
            try:
                conn, addr = server.accept()

                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()

            except Exception as e:
                print("[SERVER ERROR]", e)


if __name__ == "__main__":
    start_server()