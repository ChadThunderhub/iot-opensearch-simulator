from datetime import datetime, timezone
import time
import random
import http.client
import json
import os

HOST = os.environ.get('OPENSEARCH_HOST', 'opensearch')
PORT = int(os.environ.get('OPENSEARCH_PORT', 9200))

def tempSim():
    return round(random.uniform(10.0, 30.0), 2)

def wait_for_opensearch():
    print(f"Waiting for OpenSearch to respond @ {HOST}:{PORT}...")
    while True:
        try:
            conn = http.client.HTTPConnection(HOST, PORT)
            conn.request("GET", "/")
            resp = conn.getresponse()
            if resp.status == 200:
                print("Connection established!")
                conn.close()
                return
        except Exception:
            print("Connection failed, retrying in 5 seconds...")
            time.sleep(5)

wait_for_opensearch()

while True:
    conn = http.client.HTTPConnection(HOST, PORT)
    headers = {'Content-type': 'application/json'}
    
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(), 
        "room": "Bedroom",
        "temperature": tempSim()
    }
    
    json_data = json.dumps(data)
    
    try:
        conn.request("POST", "/sensors-v2/_doc/", json_data, headers)
        response = conn.getresponse()
        response.read()
        if response.status in [200, 201]:
            print(f"Sent data: {data}°C")
        else:
            print(f"HTTP error: {response.status}")
    except Exception as e:
        print(f"Failed to send data: {e}")
    finally:
        conn.close()
    
    time.sleep(5)
