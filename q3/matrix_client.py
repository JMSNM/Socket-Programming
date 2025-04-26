import socket
import pickle
import numpy as np

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65434

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))

        data = b""
        while True:
            part = client.recv(4096)
            if not part:
                break
            data += part
        
        rows_data, matrix_b, start_row = pickle.loads(data)

        print(f"[CLIENT] Received rows starting from row {start_row}")
        
        partial_result = np.dot(rows_data, matrix_b)

        client.sendall(pickle.dumps(partial_result))
        client.shutdown(socket.SHUT_WR)

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
