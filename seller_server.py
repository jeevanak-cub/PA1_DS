import socket, threading
from protocol import send, recv

CUST = ('localhost', 9002)
PROD = ('localhost', 9001)
HOST, PORT = '0.0.0.0', 8001

def db(addr, msg):
    s = socket.socket(); s.connect(addr)
    send(s, msg); r = recv(s); s.close()
    return r

def handle(conn):
    with conn:
        while True:
            req = recv(conn)
            if not req: break

            v = db(CUST, {'type':'VALIDATE','sid':req['sid']})
            if v['status']!='OK':
                send(conn, {'status':'ERR'})
                continue

            user = v['user']

            if req['type']=='ADD_ITEM':
                send(conn, db(PROD, {**req, 'seller':user}))

            elif req['type']=='UPDATE_PRICE':
                send(conn, db(PROD, req))

            elif req['type']=='UPDATE_QTY':
                send(conn, db(PROD, req))

            elif req['type']=='GET_SELLER_RATING':
                send(conn, db(CUST, {'type':'GET_SELLER_RATING','seller':user}))

            else:
                send(conn, {'status':'ERR'})

s = socket.socket(); s.bind((HOST,PORT)); s.listen()
print("Seller Server running")
while True:
    c,_=s.accept()
    threading.Thread(target=handle,args=(c,),daemon=True).start()
