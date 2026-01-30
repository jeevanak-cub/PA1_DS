import socket
from protocol import send, recv

CUST = ('localhost', 9002)
SELLER_SERVER = ('localhost', 8001)

s = socket.socket()
s.connect(SELLER_SERVER)
sid = None

while True:
    cmd = input('seller> ').split()

    if cmd[0] == 'register':
        t = socket.socket()
        t.connect(CUST)
        send(t, {
            'type': 'CREATE',
            'role': 'seller',
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
            'role': 'seller',
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
        'type': 'ADD_ITEM',
        'sid': sid,
        'category': 1,
        'keywords': ['a'],
        'price': 10
    })
    print(recv(s))
