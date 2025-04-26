import multiprocessing
import time
import client  

NUM_CLIENTS = 4 

def run_client():
    client.main()

def main():
    processes = []

    for _ in range(NUM_CLIENTS):
        p = multiprocessing.Process(target=run_client)
        p.start()
        processes.append(p)
        time.sleep(0.5) 

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
