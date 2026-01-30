import socket
from protocol import send, recv

CUST = ('localhost', 9002)
BUYER_SERVER = ('localhost', 8002)

s = socket.socket()
s.connect(BUYER_SERVER)
sid = None

while True:
    cmd = input('buyer> ').split()

    if cmd[0] == 'register':
        t = socket.socket()
        t.connect(CUST)
        send(t, {
            'type': 'CREATE',
            'role': 'buyer',
            'user': cmd[1],
            'pwd': cmd[2]
        })
        print(recv(t))
        t.close()
        continue

    if cmd[0] == 'login':
        t = socket.socket()
        t.connect(CUST)
        send(t, {
            'type': 'LOGIN',
            'role': 'buyer',
            'user': cmd[1],
            'pwd': cmd[2]
        })
        r = recv(t)
        t.close()
        sid = r.get('sid')
        print(r)
        continue

    if not sid:
        print("Please login first")
        continue

    send(s, {
        'type': cmd[0].upper(),
        'sid': sid,
        'category': 1,
        'keywords': ['a'],
        'item': cmd[-1] if len(cmd) > 1 else None,
        'qty': 1
    })
    print(recv(s))
