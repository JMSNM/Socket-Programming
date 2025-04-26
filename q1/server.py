import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 65432
NUM_CLIENTS = 4  

partial_sums = []
lock = threading.Lock()

def handle_client(conn, addr):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        data = conn.recv(4096)
        numbers = pickle.loads(data)

        part_sum = sum(numbers)
        print(f"[{addr}] Partial sum: {part_sum}")

        conn.sendall(pickle.dumps(part_sum))
    except Exception as e:
        print(f"[ERROR] Client {addr} - {e}")
    finally:
        conn.close()

def main():
    try:
        with open('integarsQ1.txt', 'r') as f:
            numbers = [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        print("[ERROR] File not found!")
        return

    chunk_size = len(numbers) // NUM_CLIENTS
    chunks = [numbers[i * chunk_size:(i + 1) * chunk_size] for i in range(NUM_CLIENTS)]

    if len(numbers) % NUM_CLIENTS != 0:
        chunks[-1].extend(numbers[NUM_CLIENTS * chunk_size:])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    client_threads = []
    client_sockets = []

    for chunk in chunks:
        conn, addr = server.accept()
        client_sockets.append((conn, addr))

        conn.sendall(pickle.dumps(chunk))

    total_sum = 0
    for conn, addr in client_sockets:
        data = conn.recv(4096)
        part_sum = pickle.loads(data)
        total_sum += part_sum
        conn.close()

    print(f"\n[RESULT] Total sum of all integers = {total_sum}")

if __name__ == "__main__":
    main()
