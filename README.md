# Network Analysis System - SSL Secured Multi-Client

A secure network monitoring system with SSL/TLS encryption for measuring download speeds across multiple clients.

## Quick Start

### 1. Setup (One Time)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install requests urllib3 pandas matplotlib seaborn
```

### 2. Run Server (Your Laptop)
```powershell
.venv\Scripts\activate
python server\server.py
```
Expected output: `[LISTENING] Server running on port 5000`

### 3. Run Client (Other Laptop)
Edit `client/client.py` line 16 with your server IP:
```python
{"host": "192.168.1.50", "port": 5000, "name": "local_server"}  # Your IP here
```

Then run:
```powershell
.venv\Scripts\activate
python client\client.py
```

### 4. View Results
Generate graphs:
```powershell
.venv\Scripts\activate
python visualize_data.py
```

---

## Architecture

### Server
- **File:** `server/server.py`
- **Port:** 5000
- **Certificate:** `certs/server_new.crt` & `certs/server_new.key`
- **Function:** Receives client data, stores in CSV
- **Logs:** `logs/data.csv`

### Client
- **File:** `client/client.py`
- **Certificate:** `certs/client1.crt` & `certs/client1.key`
- **Function:** Measures download speed, sends to server
- **Run:** Multiple clients simultaneously (different laptops)

### Security (SSL/TLS)
- ✅ Server verifies client certificates
- ✅ Clients verify server certificate
- ✅ Encrypted communication (port 5000)
- ✅ Uses `certs/ca.crt` (Certificate Authority)

---

## File Structure

```
project/
├── server/
│   └── server.py          # Server (listens on port 5000)
├── client/
│   └── client.py          # Client (connects to server)
├── certs/                 # SSL certificates (ready to use)
│   ├── ca.crt
│   ├── server_new.crt
│   ├── server_new.key
│   ├── client1.crt
│   └── client1.key
├── logs/
│   ├── data.csv           # Network data collected
│   └── network_analysis_graph.png  # Generated graphs
├── visualize_data.py      # Create graphs from CSV
└── README.md              # This file
```

---

## Usage Examples

### Single Client
```powershell
# Terminal 1
python server\server.py

# Terminal 2
python client\client.py
```

### Multi-Client (Different Laptops)

**Laptop A (Server):**
```powershell
python server\server.py
```

**Laptop B (Client 1):**
Edit `client.py` → IP to Laptop A
```powershell
python client\client.py
```

**Laptop C (Client 2):**
Edit `client.py` → IP to Laptop A
```powershell
python client\client.py
```

---

## Configuration

### Change Server IP (for multi-laptop)
Edit `client/client.py` line 16:
```python
SERVERS = [
    {"host": "192.168.1.50", "port": 5000, "name": "local_server"}  # Change this IP
]
```

### Find Your Server IP
```powershell
ipconfig
```
Look for `IPv4 Address` (e.g., `192.168.x.x`)

---

## Output

### CSV Data (`logs/data.csv`)
```
client_id,timestamp,download_speed_mbps
client_1,23:52:11,0.08
client_1,23:52:41,0.10
```

### Graph (`logs/network_analysis_graph.png`)
- Speed trends by client
- Speed distribution
- Average speeds
- Statistical summary

---

## SSL Certificates (Already Included)

**Already generated and ready to use:**
- ✅ `ca.crt` - Certificate Authority
- ✅ `server_new.crt` & `server_new.key` - Server certificate
- ✅ `client1.crt` & `client1.key` - Client certificate

**No action needed!** Certificates are in `certs/` folder.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Make sure server started first |
| "Certificate not found" | Check `certs/` folder exists |
| "Module not found" | Run: `pip install requests urllib3 pandas matplotlib seaborn` |
| Can't connect between laptops | Update client IP in `client.py` line 16 |

---

## Summary

1. **Server:** Run on your laptop
2. **Client:** Run on other laptops (edit IP first)
3. **View:** Run `visualize_data.py` to see graphs
4. **Secure:** All communication encrypted with SSL/TLS

Ready to go! 
 