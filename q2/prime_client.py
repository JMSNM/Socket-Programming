import socket
import pickle
import math

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65433

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        
        data = client.recv(1024)
        number = pickle.loads(data)

        print(f"[CLIENT] Checking if {number} is prime...")
        prime = is_prime(number)

        result = "PRIME" if prime else "NOT PRIME"
        client.sendall(pickle.dumps(result))
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
