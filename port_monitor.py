# File: port_monitor.py
# Location: /projects/midnight-infrastructure/

from fastapi import FastAPI
import psutil

app = FastAPI()

PORT_MAP = {
    3000: "midnight-infrastructure",
    4000: "star-stats",
    5000: "quantum-resonance"
}

@app.get("/api/ports")
def get_ports():
    active_ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN':
            port = conn.laddr.port
            if port in PORT_MAP:
                active_ports.append({
                    "project": PORT_MAP[port],
                    "port": port,
                    "status": "active"
                })
    return active_ports