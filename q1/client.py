import socket
import pickle

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        
        data = client.recv(4096)
        numbers = pickle.loads(data)

        part_sum = sum(numbers)

        client.sendall(pickle.dumps(part_sum))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
