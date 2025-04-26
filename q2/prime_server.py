import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 65433
TIMEOUT = 10  

numbers_to_check = [
    15485863, 15485867, 15485869, 15485871, 15485873, 
    15485877, 15485879, 15485881  
]

results = {}

def handle_client(conn, addr, number):
    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        conn.settimeout(TIMEOUT) 

        conn.sendall(pickle.dumps(number))

        data = conn.recv(1024)
        result = pickle.loads(data)

        results[number] = result
        print(f"[{addr}] Number {number} is {result}")
    except socket.timeout:
        print(f"[TIMEOUT] Client {addr} took too long. Marking {number} as 'No Response'.")
        results[number] = "No Response"
    except Exception as e:
        print(f"[ERROR] Client {addr} - {e}")
        results[number] = "Error"
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    client_threads = []

    for number in numbers_to_check:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, number))
        thread.start()
        client_threads.append(thread)

    for t in client_threads:
        t.join()

    print("\n[RESULTS]")
    for number, status in results.items():
        print(f"{number}: {status}")

if __name__ == "__main__":
    main()
