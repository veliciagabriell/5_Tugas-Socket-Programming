import socket
import threading
import queue

class ChatServer:
    def __init__(self, host="10.8.102.85", port=8081):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)
        self.messages = queue.Queue()
        self.clients = []  # List to keep track of connected clients
        print(f"Server is running on {host}:{port}")

    def receive(self):
        """Receive messages from clients."""
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                print(f"Received message: {message.decode()} from {addr}")
                self.messages.put((message, addr))
            except Exception as e:
                print(f"Error receiving message: {e}")

    def broadcast(self):
        while True:
            while not self.messages.empty():
                message, addr = self.messages.get()
                try:
                    message_decoded = message.decode()  # Decode once
                    if message_decoded.startswith("SIGNUP_TAG: "):
                        name = message_decoded.split(": ")[1]
                        self.clients.append(addr)  # Add the client to the list
                        join_message = f"{name} joined the chat!"
                        print(join_message)  # Debug log
                        # Broadcast the join message to all clients
                        for client in self.clients:
                            self.server_socket.sendto(join_message.encode(), client)
                    else:
                        print(f"Message from {addr}: {message_decoded}")
                        for client in self.clients:
                            try:
                                print(f"Sending to {client}")
                                self.server_socket.sendto(message, client)
                            except Exception as e:
                                print(f"Error sending to {client}: {e}")
                                if client in self.clients:
                                    self.clients.remove(client)  # Remove the client if an error occurs
                except UnicodeDecodeError:
                    print("Failed to decode message, skipping...")

    def start(self):
        """Start the server threads."""
        t1 = threading.Thread(target=self.receive, daemon=True)
        t2 = threading.Thread(target=self.broadcast, daemon=True)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
