import socket, threading, uuid
from protocol import send, recv

products = {}
LOCK = threading.Lock()
HOST, PORT = "0.0.0.0", 9001


def handle(conn):
    with conn:
        while True:
            req = recv(conn)
            if not req:
                break
            send(conn, process(req))


def process(req):
    with LOCK:
        if req['type'] == 'ADD_ITEM':
            iid = f"{req['category']}-{uuid.uuid4().hex[:6]}"
            products[iid] = {**req, 'item_id': iid, 'feedback': [0,0]}
            return {'status': 'OK', 'item_id': iid}

        if req['type'] == 'SEARCH':
            res = []
            for p in products.values():
                if p['category'] == req['category'] and any(k in p['keywords'] for k in req['keywords']):
                    res.append(p)
            return {'status': 'OK', 'results': res}

        if req['type'] == 'GET_ITEM':
            return {'status': 'OK', 'item': products.get(req['item'])}

        return {'status': 'ERR'}


s = socket.socket(); s.bind((HOST, PORT)); s.listen()
print('Product DB running')
while True:
    c,_ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()