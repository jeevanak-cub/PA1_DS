import json


def send(sock, obj):
    sock.sendall((json.dumps(obj) + "\n").encode())


def recv(sock):
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            return None
        data += chunk
    line, _ = data.split(b"\n", 1)
    return json.loads(line.decode())




