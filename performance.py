import socket
import time
import threading
from protocol import send, recv


BUYER_SERVER = ('localhost', 8002)
SELLER_SERVER = ('localhost', 8001)
CUSTOMER_DB = ('localhost', 9002)

OPS_PER_CLIENT = 1000
NUM_RUNS = 10
CONNECT_DELAY = 0.001

lock = threading.Lock()



def login(role, user, pwd):
    s = socket.socket()
    s.connect(CUSTOMER_DB)
    send(s, {
        'type': 'LOGIN',
        'role': role,
        'user': user,
        'pwd': pwd
    })
    resp = recv(s)
    s.close()

    if not resp or resp.get('status') != 'OK':
        raise RuntimeError(f"{role} login failed: {resp}")

    return resp['sid']



def buyer_worker(response_times):
    try:
        sid = login('buyer', 'buyer1', 'pass1')
    except Exception:
        return

    for _ in range(OPS_PER_CLIENT):
        try:
            s = socket.socket()
            s.connect(BUYER_SERVER)

            start = time.time()
            send(s, {'type': 'GET_CART', 'sid': sid})
            recv(s)
            end = time.time()

            with lock:
                response_times.append(end - start)

            s.close()
            time.sleep(CONNECT_DELAY)
        except Exception:
            pass


def seller_worker(response_times):
    try:
        sid = login('seller', 'seller1', 'pass1')
    except Exception:
        return

    for _ in range(OPS_PER_CLIENT):
        try:
            s = socket.socket()
            s.connect(SELLER_SERVER)

            start = time.time()
            send(s, {
                'type': 'ADD_ITEM',
                'sid': sid,
                'category': 1,
                'keywords': ['perf'],
                'price': 10
            })
            recv(s)
            end = time.time()

            with lock:
                response_times.append(end - start)

            s.close()
            time.sleep(CONNECT_DELAY)
        except Exception:
            pass


def single_run(num_buyers, num_sellers):
    response_times = []
    threads = []

    start_time = time.time()

    for _ in range(num_buyers):
        t = threading.Thread(target=buyer_worker, args=(response_times,))
        threads.append(t)
        t.start()
        time.sleep(0.005)

    for _ in range(num_sellers):
        t = threading.Thread(target=seller_worker, args=(response_times,))
        threads.append(t)
        t.start()
        time.sleep(0.005)

    for t in threads:
        t.join()

    end_time = time.time()

    if len(response_times) == 0:
        raise RuntimeError("No successful API calls recorded")

    total_ops = (num_buyers + num_sellers) * OPS_PER_CLIENT
    total_time = end_time - start_time

    avg_response_time = sum(response_times) / len(response_times)
    throughput = total_ops / total_time

    return avg_response_time, throughput


def run_experiment(num_buyers, num_sellers):
    response_time_runs = []
    throughput_runs = []

    print()
    for run in range(NUM_RUNS):
        avg_rt, th = single_run(num_buyers, num_sellers)
        response_time_runs.append(avg_rt)
        throughput_runs.append(th)

        print(
            f"run {run+1}/{NUM_RUNS}: "
            f"avg_resp={avg_rt:.5f}s, "
            f"throughput={th:.2f} ops/s"
        )

    print("\n---- Averages over runs ----")
    print(f"Scenario 1: sellers={num_sellers}, buyers={num_buyers}")
    print(f"Average response time (s/op): {sum(response_time_runs)/NUM_RUNS:.5f}")
    print(f"Average throughput (ops/s): {sum(throughput_runs)/NUM_RUNS:.2f}")



if __name__ == "__main__":
    #run_experiment(100, 100)
    run_experiment(1, 1)
    #run_experiment(10, 10)
    # run_experiment(100, 100)
