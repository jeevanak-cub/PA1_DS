import socket
from protocol import send, recv

SERVER=('localhost',8002)
CUST=('localhost',9002)
sid=None

def login(user,pwd):
    global sid
    s=socket.socket(); s.connect(CUST)
    send(s,{'type':'LOGIN','role':'buyer','user':user,'pwd':pwd})
    r=recv(s); s.close()
    sid=r.get('sid')
    print(r)

while True:
    cmd=input("buyer> ").split()
    if cmd[0]=='login': login(cmd[1],cmd[2]); continue
    if not sid: print("login first"); continue

    s=socket.socket(); s.connect(SERVER)

    if cmd[0]=='search':
        send(s,{'type':'SEARCH','sid':sid,'category':1,'keywords':['a']})
    elif cmd[0]=='cart':
        send(s,{'type':'ADD_CART','sid':sid,'item':cmd[1],'qty':1})
    elif cmd[0]=='show':
        send(s,{'type':'GET_CART','sid':sid})
    else:
        print("Unknown"); continue

    print(recv(s))
    s.close()
