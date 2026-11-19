import json
import socket
import threading
import time 

DISCOVERY_PORT = 50000   # clients listens for pings on this UDP port
BUFFER_SIZE = 4096
DISCOVERY_TIMEOUT = 2 # waiting time for replies 


def make_listener_socket():
    """Binding a socket to listen for pings"""
    # create udp socket bound to discovery port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # let two clients on the same machine both bind the same port (for local testing)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("", DISCOVERY_PORT))   # "" means listen on every network interface
    return sock


def listen(my_email):
    """Get pings and respond with pongs"""
    # answer every ping, saying who is responding 
    sock = make_listener_socket()
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)   # addr is the senders (ip, port)
        try:
            msg = json.loads(data.decode())
        except (ValueError, UnicodeDecodeError):
            continue   # ignore anything that isn't our JSON format

        # don't answer our own broadcast
        if msg.get("type") == "ping" and msg.get("email") != my_email:
            reply = {"type": "pong", "email": my_email}
            sock.sendto(json.dumps(reply).encode(), addr)


def start_listener(my_email):
    """Starts listening for pings to check online contacts"""
    # run in background so it doesnt interfere with the shell
    thread = threading.Thread(target=listen, args=(my_email,), daemon=True)
    thread.start()

def discover(my_email):
    # Broadcast a ping and collect replies, returns {email: ip} for everyone who answered
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   # allow sending to the broadcast address

    ping = {"type": "ping", "email": my_email}
    sock.sendto(json.dumps(ping).encode(), ("255.255.255.255", DISCOVERY_PORT))

    online = {}
    deadline = time.monotonic() + DISCOVERY_TIMEOUT
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        sock.settimeout(remaining)   # wait only as long as is left
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
        except socket.timeout:
            break
        try:
            msg = json.loads(data.decode())
        except (ValueError, UnicodeDecodeError):
            continue
        if msg.get("type") == "pong" and "email" in msg:
            online[msg["email"]] = addr[0]   # remember their IP for sending files later

    sock.close()
    return online