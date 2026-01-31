import socket
from protocol import send, recv

SERVER=('localhost',8001)
CUST=('localhost',9002)

sid=None

def login(user,pwd):
    global sid
    s=socket.socket(); s.connect(CUST)
    send(s,{'type':'LOGIN','role':'seller','user':user,'pwd':pwd})
    r=recv(s); s.close()
    sid=r.get('sid')
    print(r)

while True:
    cmd=input("seller> ").split()
    if cmd[0]=='login': login(cmd[1],cmd[2]); continue
    if not sid: print("login first"); continue

    s=socket.socket(); s.connect(SERVER)

    if cmd[0]=='add':
        send(s,{'type':'ADD_ITEM','sid':sid,'name':cmd[1],'category':1,'keywords':['a'],'condition':'new','price':10,'qty':5})
    elif cmd[0]=='price':
        send(s,{'type':'UPDATE_PRICE','sid':sid,'item':cmd[1],'price':int(cmd[2])})
    elif cmd[0]=='qty':
        send(s,{'type':'UPDATE_QTY','sid':sid,'item':cmd[1],'delta':int(cmd[2])})
    else:
        print("Unknown")
        continue

    print(recv(s))
    s.close()
