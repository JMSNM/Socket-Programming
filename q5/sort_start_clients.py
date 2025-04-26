from multiprocessing import Process
import time
import sort_client

def run_client():
    sort_client.main()

if __name__ == "__main__":
    num_clients = 4 
    processes = []

    for _ in range(num_clients):
        p = Process(target=run_client)
        p.start()
        processes.append(p)
        time.sleep(0.5) 

    for p in processes:
        p.join()
