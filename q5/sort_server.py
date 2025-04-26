import socket
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


def simple_merge(sorted_chunks):
    result = []
    for chunk in sorted_chunks:
        result.extend(chunk)
    return sorted(result)

def parallel_merge(sorted_chunks):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(lambda chunks: sorted([item for sublist in chunks for item in sublist]), sorted_chunks)
        return future.result()


def handle_client(client_socket, chunk, results, index):
    try:
        client_socket.sendall(chunk.encode())
        data = client_socket.recv(8192).decode()
        results[index] = list(map(int, data.split(',')))
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()

    print("Server listening on 127.0.0.1 5555")

    num_clients = 4
    results = [None] * num_clients

    array = list(range(1, 10001))
    array.reverse()  

    chunk_size = len(array) // num_clients
    chunks = [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]

    threads = []
    for i in range(num_clients):
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, ','.join(map(str, chunks[i])), results, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    sorted_chunks = [sorted(chunk) for chunk in results] 
    start_time = time.time()
    final_sorted = simple_merge(sorted_chunks)
    end_time = time.time()
    print(f"Simple merge took {end_time - start_time} seconds")

    start_time = time.time()
    final_sorted_parallel = parallel_merge(sorted_chunks)
    end_time = time.time()
    print(f"Parallel merge took {end_time - start_time} seconds")

    if final_sorted == final_sorted_parallel:
        print("Both merges gave the same result.")
    else:
        print("Merging results do not match!")

if __name__ == "__main__":
    main()
