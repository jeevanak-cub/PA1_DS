import socket, threading
from protocol import send, recv

CUST=('localhost',9002)
PROD=('localhost',9001)
HOST,PORT='0.0.0.0',8002

def db(addr,msg):
    s=socket.socket(); s.connect(addr)
    send(s,msg); r=recv(s); s.close(); return r

def handle(conn):
    with conn:
        while True:
            req=recv(conn)
            if not req: break

            v=db(CUST,{'type':'VALIDATE','sid':req['sid']})
            if v['status']!='OK':
                send(conn,{'status':'ERR'})
                continue

            user=v['user']

            if req['type']=='SEARCH':
                send(conn, db(PROD, req))

            elif req['type']=='GET_ITEM':
                send(conn, db(PROD, req))

            elif req['type']=='ADD_CART':
                send(conn, db(CUST,{**req,'user':user}))

            elif req['type']=='REMOVE_CART':
                send(conn, db(CUST,{**req,'user':user}))

            elif req['type']=='GET_CART':
                send(conn, db(CUST,{'type':'GET_CART','user':user}))

            elif req['type']=='CLEAR_CART':
                send(conn, db(CUST,{'type':'CLEAR_CART','user':user}))

            elif req['type']=='FEEDBACK':
                send(conn, db(CUST,{'type':'SELLER_FEEDBACK','seller':req['seller'],'vote':req['vote']}))

            elif req['type']=='GET_PURCHASES':
                send(conn, db(CUST,{'type':'GET_PURCHASES','user':user}))

            else:
                send(conn,{'status':'ERR'})

s=socket.socket(); s.bind((HOST,PORT)); s.listen()
print("Buyer Server running")
while True:
    c,_=s.accept()
    threading.Thread(target=handle,args=(c,),daemon=True).start()
