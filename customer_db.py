import socket, threading, time, uuid
from protocol import send, recv

buyers, sellers = {}, {}
sessions, carts, purchases = {}, {}, {}
seller_feedback = {}
LOCK = threading.Lock()
TIMEOUT = 300
HOST, PORT = "0.0.0.0", 9002

def cleanup():
    while True:
        time.sleep(30)
        with LOCK:
            now = time.time()
            for sid in list(sessions):
                if now - sessions[sid]['last'] > TIMEOUT:
                    del sessions[sid]

def process(req):
    with LOCK:
        t = req['type']

        if t == 'CREATE':
            store = buyers if req['role']=='buyer' else sellers
            store[req['user']] = req['pwd']
            if req['role']=='seller':
                seller_feedback[req['user']] = [0,0]
            return {'status':'OK'}

        if t == 'LOGIN':
            store = buyers if req['role']=='buyer' else sellers
            if store.get(req['user']) == req['pwd']:
                sid = uuid.uuid4().hex
                sessions[sid]={'user':req['user'],'role':req['role'],'last':time.time()}
                carts.setdefault(req['user'],{})
                purchases.setdefault(req['user'],[])
                return {'status':'OK','sid':sid}
            return {'status':'ERR'}

        if t == 'VALIDATE':
            s = sessions.get(req['sid'])
            if not s: return {'status':'ERR'}
            s['last']=time.time()
            return {'status':'OK','user':s['user'],'role':s['role']}

        if t == 'ADD_CART':
            carts[req['user']][req['item']] = carts[req['user']].get(req['item'],0)+req['qty']
            return {'status':'OK'}

        if t == 'REMOVE_CART':
            carts[req['user']][req['item']] -= req['qty']
            return {'status':'OK'}

        if t == 'GET_CART':
            return {'status':'OK','cart':carts[req['user']]}

        if t == 'CLEAR_CART':
            carts[req['user']]={}
            return {'status':'OK'}

        if t == 'ADD_PURCHASE':
            purchases[req['user']].append(req['item'])
            return {'status':'OK'}

        if t == 'GET_PURCHASES':
            return {'status':'OK','items':purchases[req['user']]}

        if t == 'SELLER_FEEDBACK':
            fb=seller_feedback[req['seller']]
            fb[0 if req['vote']=='up' else 1]+=1
            return {'status':'OK'}

        if t == 'GET_SELLER_RATING':
            return {'status':'OK','rating':seller_feedback.get(req['seller'],[0,0])}

        return {'status':'ERR'}

def handle(conn):
    with conn:
        while True:
            req=recv(conn)
            if not req: break
            send(conn,process(req))

threading.Thread(target=cleanup,daemon=True).start()
s=socket.socket(); s.bind((HOST,PORT)); s.listen()
print("Customer DB running")
while True:
    c,_=s.accept()
    threading.Thread(target=handle,args=(c,),daemon=True).start()
