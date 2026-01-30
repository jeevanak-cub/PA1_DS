import socket, threading, time, uuid
from protocol import send, recv

buyers = {}
sellers = {}
sessions = {}
carts = {}
purchases = {}
LOCK = threading.Lock()
TIMEOUT = 300
HOST, PORT = "0.0.0.0", 9002


def cleanup_sessions():
    while True:
        time.sleep(30)
        with LOCK:
            now = time.time()
            for sid in list(sessions.keys()):
                if now - sessions[sid]['last'] > TIMEOUT:
                    del sessions[sid]


def handle(conn):
    with conn:
        while True:
            req = recv(conn)
            if not req:
                break
            send(conn, process(req))


def process(req):
    with LOCK:
        t = req['type']

        if t == 'CREATE':
            role = req['role']
            store = buyers if role == 'buyer' else sellers
            store[req['user']] = req['pwd']
            return {'status': 'OK'}

        if t == 'LOGIN':
            store = buyers if req['role'] == 'buyer' else sellers
            if store.get(req['user']) == req['pwd']:
                sid = uuid.uuid4().hex
                sessions[sid] = {'user': req['user'], 'role': req['role'], 'last': time.time()}
                carts.setdefault(req['user'], {})
                purchases.setdefault(req['user'], [])
                return {'status': 'OK', 'sid': sid}
            return {'status': 'ERR'}

        if t == 'VALIDATE':
            s = sessions.get(req['sid'])
            if not s:
                return {'status': 'ERR'}
            s['last'] = time.time()
            return {'status': 'OK', 'user': s['user']}

        if t == 'ADD_CART':
            carts[req['user']][req['item']] = carts[req['user']].get(req['item'], 0) + req['qty']
            return {'status': 'OK'}

        if t == 'GET_CART':
            return {'status': 'OK', 'cart': carts.get(req['user'], {})}

        if t == 'CLEAR_CART':
            carts[req['user']] = {}
            return {'status': 'OK'}

        if t == 'ADD_PURCHASE':
            purchases[req['user']].append(req['item'])
            return {'status': 'OK'}

        if t == 'GET_PURCHASES':
            return {'status': 'OK', 'items': purchases.get(req['user'], [])}

        return {'status': 'ERR'}


threading.Thread(target=cleanup_sessions, daemon=True).start()
s = socket.socket(); s.bind((HOST, PORT)); s.listen()
print('Customer DB running')
while True:
    c,_ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()

