import socket
import threading

class ChatServer:
    def __init__(self, host='10.5.102.117', port=8081):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((host, port))
        self.clients = set()
        print(f"Chat server started on {host}:{port}")

    def handle_client(self):
        """Handle incoming messages from clients."""
        while True:
            try:
                message, client_address = self.server_socket.recvfrom(1024)
                if client_address not in self.clients:
                    self.clients.add(client_address)
                    print(f"New client joined: {client_address}")

                print(f"Received message from {client_address}: {message.decode()}")
                
                # Send acknowledgment back to the client
                ack_message = "ACK"
                self.server_socket.sendto(ack_message.encode(), client_address)

                # Broadcast the message to other clients
                self.broadcast(message, client_address)
            except Exception as e:
                print(f"Error handling client: {e}")

    def broadcast(self, message, sender_address):
        """Send a message to all clients except the sender."""
        for client in self.clients:
            if client != sender_address:
                self.server_socket.sendto(message, client)

    def start(self):
        """Start the server."""
        self.handle_client()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
