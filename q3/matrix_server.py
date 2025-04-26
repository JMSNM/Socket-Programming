import socket
import threading
import pickle
import numpy as np

HOST = '127.0.0.1'
PORT = 65434
NUM_CLIENTS = 4  

partial_results = {}

def handle_client(conn, addr, rows_data, matrix_b, start_row):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        
        payload = pickle.dumps((rows_data, matrix_b, start_row))
        conn.sendall(payload)
        conn.shutdown(socket.SHUT_WR)  
        
        data = b""
        conn.settimeout(10) 
        while True:
            try:
                part = conn.recv(4096)
                if not part:
                    break
                data += part
            except socket.timeout:
                print(f"[TIMEOUT] Client {addr} did not send full data in time.")
                break
        
        if data:
            partial = pickle.loads(data)
            partial_results[start_row] = partial
            print(f"[{addr}] Partial matrix received starting at row {start_row}")
        else:
            print(f"[ERROR] No data received from {addr}")

    except Exception as e:
        print(f"[ERROR] Client {addr} - {e}")
    finally:
        conn.close()



def main():
    A = np.random.randint(1, 10, (8, 6))  # 8x6
    B = np.random.randint(1, 10, (6, 5))  # 6x5

    if A.shape[1] != B.shape[0]:
        print("[ERROR] Matrix dimensions do not match for multiplication!")
        return

    print("[SERVER] Matrices generated.")
    print("Matrix A:")
    print(A)
    print("Matrix B:")
    print(B)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    client_threads = []

    rows_per_client = len(A) // NUM_CLIENTS
    extra_rows = len(A) % NUM_CLIENTS
    start = 0

    for i in range(NUM_CLIENTS):
        end = start + rows_per_client + (1 if i < extra_rows else 0)
        rows_data = A[start:end]

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, rows_data, B, start))
        thread.start()
        client_threads.append(thread)

        start = end

    for t in client_threads:
        t.join()

    sorted_starts = sorted(partial_results.keys())
    result_matrix = np.vstack([partial_results[start] for start in sorted_starts])

    print("\n[FINAL RESULT] Product Matrix C = A x B")
    print(result_matrix)

if __name__ == "__main__":
    main()
