import socket
import threading
import queue
import time

class ChatServer:
    DEFAULT_PORT = 8083

    def __init__(self, host="0.0.0.0", port=DEFAULT_PORT):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)
        self.messages = queue.Queue()
        self.clients = []
        self.username = {}
        print(f"Server berjalan di {host}:{port}")

    def receive(self):
        """Menerima pesan dari klien and mengatur nama."""
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                decoded_message = message.decode()
                print(f"Menerima pesan: {decoded_message} dari {addr}")

                if addr not in self.username:  
                    if decoded_message.startswith("CEK_NAMA:"):
                        username = decoded_message.split(":")[1].strip()
                        
                        if username in self.username.values() and self.username.get(addr) != username: 
                            print(f"Nama '{username}' sudah terpakai. Memberi tahu klien {addr}.")
                            self.server_socket.sendto("NAMA_SUDAH_TERPAKAI".encode(), addr)
                        else:
                            self.username[addr] = username
                            if addr not in self.clients:
                                self.clients.append(addr)
                            self.server_socket.sendto("NAMA_DITERIMA".encode(), addr)
                            print(f"Nama '{username}' diterima dari {addr}")
                    continue

                user_message = f"{self.username[addr]}: {decoded_message}"
                self.messages.put((user_message.encode(), addr))
                print(f"Pesan dari {self.username[addr]} ditambahkan ke antrean")

            except Exception as e:
                print(f"Error dari {addr}: {e}")

    def broadcast(self):
        """Broadcast messages to all connected clients."""
        while True:
            while not self.messages.empty():
                message, addr = self.messages.get()
                disconnected_clients = []
                
                for client in self.clients:
                    if client != addr:
                        try:
                            self.server_socket.sendto(message, client)
                            print(f"Mengirim pesan ke {client}")
                        except Exception as e:
                            print(f"Error mengirim pesan ke {client}: {e}")
                            disconnected_clients.append(client)
                
                for client in disconnected_clients:
                    self.clients.remove(client)
                    username = self.username.pop(client, "Unknown")
                    print(f"Klien terputus {client} ({username}) telah dihapus")
                
                time.sleep(0.01)

    def start(self):
        """Start the server threads."""
        receive_thread = threading.Thread(target=self.receive, daemon=True)
        broadcast_thread = threading.Thread(target=self.broadcast, daemon=True)
        receive_thread.start()    
        broadcast_thread.start()
        receive_thread.join()
        broadcast_thread.join()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()