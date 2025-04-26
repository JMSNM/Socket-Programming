import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    data = client.recv(8192).decode()

    chunk = list(map(int, data.split(',')))
    sorted_chunk = sorted(chunk)  

    client.send(','.join(map(str, sorted_chunk)).encode())
    client.close()

if __name__ == "__main__":
    main()
