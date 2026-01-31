import socket, threading, uuid
from protocol import send, recv

products={}
LOCK=threading.Lock()
HOST,PORT="0.0.0.0",9001

def process(req):
    with LOCK:
        t=req['type']

        if t=='ADD_ITEM':
            iid=f"{req['category']}-{uuid.uuid4().hex[:6]}"
            products[iid]={
                'item_id':iid,
                'name':req['name'],
                'seller':req['seller'],
                'category':req['category'],
                'keywords':req['keywords'],
                'condition':req['condition'],
                'price':req['price'],
                'qty':req['qty'],
                'feedback':[0,0]
            }
            return {'status':'OK','item_id':iid}

        if t=='SEARCH':
            res=[p for p in products.values()
                 if p['category']==req['category']
                 and any(k in p['keywords'] for k in req['keywords'])]
            return {'status':'OK','results':res}

        if t=='GET_ITEM':
            return {'status':'OK','item':products.get(req['item'])}

        if t=='UPDATE_PRICE':
            products[req['item']]['price']=req['price']
            return {'status':'OK'}

        if t=='UPDATE_QTY':
            products[req['item']]['qty']+=req['delta']
            return {'status':'OK'}

        return {'status':'ERR'}

def handle(conn):
    with conn:
        while True:
            req=recv(conn)
            if not req: break
            send(conn,process(req))

s=socket.socket(); s.bind((HOST,PORT)); s.listen()
print("Product DB running")
while True:
    c,_=s.accept()
    threading.Thread(target=handle,args=(c,),daemon=True).start()
