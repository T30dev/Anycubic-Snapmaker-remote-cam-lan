import json
import time
from websocket import create_connection

# =========================
# CONFIGURATION
# =========================

PRINTER_IP = "PRINTER_IP"
TOKEN = "API_TOKEN"
INTERVAL = 2
# Seconds between keepalive signals
# Recommended: 2-5

WS_URL = f"ws://{PRINTER_IP}/websocket?token={TOKEN}"

payload = {
    "id": 1000,
    "jsonrpc": "2.0",
    "method": "camera.start_monitor",
    "params": {
        "domain": "lan",
        "interval": 0
    }
}

print("=====================================")
print(" Snapmaker U1 Camera KeepAlive")
print("=====================================")
print("Printer:", PRINTER_IP)
print("Interval:", INTERVAL,"seconds")
print("Starting...")

while True:

    try:
        ws = create_connection(WS_URL, timeout=5)

        ws.send(json.dumps(payload))

        try:
            ws.recv()
            print(time.strftime("%H:%M:%S"),"camera alive")

        except:
            print(time.strftime("%H:%M:%S"),"signal sent")

        ws.close()

    except Exception as e:

        print(time.strftime("%H:%M:%S"),"error:",e)

    time.sleep(INTERVAL)