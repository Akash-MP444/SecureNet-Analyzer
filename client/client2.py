import socket
import ssl
import json
import time
import requests
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SERVERS = [
    {"host": "127.0.0.1", "port": 5000, "name": "local_server"},
]

CLIENT_ID = "client_2"
CLIENT_CERT = "certs/client2.crt"
CLIENT_KEY = "certs/client2.key"
CA_CERT = "certs/ca.crt"

RUN_DURATION = 120

def measure_download_speed():
    url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        end = time.time()
        file_size = len(response.content)
        time_taken = end - start
        speed_mbps = (file_size * 8) / (time_taken * 1_000_000)
        return round(speed_mbps, 2)
    except Exception as e:
        print("[DOWNLOAD ERROR]", e)
        return 0

def send_data():
    speed = measure_download_speed()
    data = {
        "client_id": CLIENT_ID,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "download_speed_mbps": speed
    }
    print(f"[SENDING] {data}")
    for server in SERVERS:
        try:
            print(f"[CONNECTING] to {server['name']} at {server['host']}:{server['port']}")
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
            context.load_verify_locations(CA_CERT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_REQUIRED
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            secure_sock = context.wrap_socket(sock, server_hostname=server['host'])
            secure_sock.connect((server['host'], server['port']))
            secure_sock.send(json.dumps(data).encode())
            response = secure_sock.recv(1024).decode()
            print(f"[SERVER RESPONSE from {server['name']}] {response}")
            secure_sock.close()
            print(f"[SUCCESS] Data sent to {server['name']}")
        except Exception as e:
            print(f"[CLIENT ERROR connecting to {server['name']}] {e}")
            continue

if __name__ == "__main__":
    start_time = time.time()
    try:
        while True:
            if time.time() - start_time > RUN_DURATION:
                print("Demo finished (5 minutes).")
                break
            send_data()
            time.sleep(20)
    except KeyboardInterrupt:
        print("\nStopped manually.")