import socket
from collections import defaultdict
import string

def process_chunk(chunk):
    word_count = defaultdict(int)
    chunk = chunk.translate(str.maketrans('', '', string.punctuation)).lower()
    words = chunk.split()
    for word in words:
        word_count[word] += 1
    return word_count

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    data = client.recv(8192).decode()

    word_count = process_chunk(data)
    client.send(str(dict(word_count)).encode())
    client.close()

if __name__ == "__main__":
    main()
