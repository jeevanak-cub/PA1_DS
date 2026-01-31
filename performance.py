import socket, time, threading, random
from protocol import send, recv

BUYER_SERVER=('localhost',8002)
SELLER_SERVER=('localhost',8001)
CUST=('localhost',9002)

OPS_PER_CLIENT=1000
NUM_RUNS=10
lock=threading.Lock()

def login(role,user):
    s=socket.socket(); s.connect(CUST)

    send(s,{'type':'LOGIN','role':role,'user':user,'pwd':'pass'})
    r=recv(s)

    if r.get('status')!='OK':
        send(s,{'type':'CREATE','role':role,'user':user,'pwd':'pass'})
        recv(s)
        send(s,{'type':'LOGIN','role':role,'user':user,'pwd':'pass'})
        r=recv(s)

    s.close()
    return r['sid']


def buyer_worker(times):
    sid=login('buyer','buyer1')
    for _ in range(OPS_PER_CLIENT):
        s=socket.socket(); s.connect(BUYER_SERVER)
        op=random.choice(['SEARCH','GET_CART'])
        start=time.time()
        send(s,{'type':op,'sid':sid,'category':1,'keywords':['a']})
        recv(s)
        end=time.time()
        with lock: times.append(end-start)
        s.close()

def seller_worker(times):
    sid=login('seller','seller1')
    for _ in range(OPS_PER_CLIENT):
        s=socket.socket(); s.connect(SELLER_SERVER)
        start=time.time()
        send(s,{'type':'ADD_ITEM','sid':sid,'name':'p','category':1,'keywords':['a'],'condition':'new','price':5,'qty':1})
        recv(s)
        end=time.time()
        with lock: times.append(end-start)
        s.close()

def run_scenario(buyers,sellers):
    times=[]
    threads=[]
    start=time.time()

    for _ in range(buyers):
        t=threading.Thread(target=buyer_worker,args=(times,)); t.start(); threads.append(t)
    for _ in range(sellers):
        t=threading.Thread(target=seller_worker,args=(times,)); t.start(); threads.append(t)

    for t in threads: t.join()
    end=time.time()

    avg_rt=sum(times)/len(times)
    throughput=(buyers+sellers)*OPS_PER_CLIENT/(end-start)
    return avg_rt,throughput

if __name__=="__main__":
    for scenario in [(1,1),(10,10),(100,100)]:
        print(f"\nScenario {scenario}")
        rts,ths=[],[]
        for _ in range(NUM_RUNS):
            rt,th=run_scenario(*scenario)
            rts.append(rt); ths.append(th)
        print("Avg RT:",sum(rts)/NUM_RUNS)
        print("Throughput:",sum(ths)/NUM_RUNS)
