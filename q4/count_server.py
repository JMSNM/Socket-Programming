import socket
import threading
from collections import defaultdict

def split_text_into_chunks(text, num_chunks):
    words = text.split()
    avg = len(words) // num_chunks
    chunks = []
    for i in range(num_chunks):
        start = i * avg
        end = (i + 1) * avg if i != num_chunks - 1 else len(words)
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
    return chunks

def handle_client(client_socket, chunk, results, index):
    try:
        # Send the chunk to the client
        client_socket.sendall(chunk.encode())

        # Receive word count result (receive once)
        data = client_socket.recv(8192)  # receive all data in one go
        partial_count = eval(data.decode())  # CAUTION: unsafe in real projects

        results[index] = partial_count
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()

    print("Server listening on 127.0.0.1 5555")

    num_clients = 4  # 🔥 make sure client count matches
    results = [None] * num_clients

    # Load text file
    with open('large_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    chunks = split_text_into_chunks(text, num_clients)

    threads = []
    for i in range(num_clients):
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, chunks[i], results, i))
        thread.start()
        threads.append(thread)

    # Wait for all client threads
    for thread in threads:
        thread.join()

    # Merge all partial results
    merged_word_count = defaultdict(int)
    for partial in results:
        for word, count in partial.items():
            merged_word_count[word] += count

    # Display top N most frequent words
    N = 10
    top_words = sorted(merged_word_count.items(), key=lambda x: x[1], reverse=True)[:N]
    print("\nTop words:")
    for word, freq in top_words:
        print(f"{word}: {freq}")

if __name__ == "__main__":
    main()
