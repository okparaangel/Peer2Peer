# Create a detail operation on how p2p protocol works
import socket
import threading

class PeerToPeerProtocol:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)

    def run(self):
        print(f"Listening for connections on {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            print(f"Connected to {addr}")
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message.startswith("HELLO"):
                self.peers.append(conn)
                print(f"Peer {conn.getpeername()} added to the network")
                file_name = message.split()[1]
                self.send_file(conn, file_name)
            elif message.startswith("SEND_FILE"):
                file_name = message.split()[1]
                self.receive_file(conn, file_name)
        conn.close()

    def send_file(self, conn, file_name):
        try:
            with open(file_name, "rb") as file:
                data = file.read()
                conn.sendall(data)
        except FileNotFoundError:
            conn.sendall(b"File not found")

    def receive_file(self, conn, file_name):
        with open(file_name, "wb") as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)

if __name__ == "__main__":
    host = "localhost"
    port = 12345
    p2p_protocol = PeerToPeerProtocol(host, port)
    p2p_protocol.run()
