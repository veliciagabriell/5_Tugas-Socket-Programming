import socket
import threading
import queue

class ChatServer:
    def __init__(self, host="0.0.0.0", port=8081):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)
        self.messages = queue.Queue()
        self.clients = []  # List to keep track of connected clients
        self.username = {}
        print(f"Server is running on {host}:{port}")

    def receive(self):
        # """Receive messages from clients."""
        # while True:
        #     try:
        #         message, addr = self.server_socket.recvfrom(1024)
        #         if addr not in self.clients:
        #             self.clients.append(addr)  # Add the new client to the list
        #             print(f"New client connected: {addr}")

        #         decoded_message = message.decode()
        #         print(f"Received message from {addr}: {decoded_message}")
        #         self.messages.put((message, addr))
        #     except Exception as e:
        #         print(f"Error receiving message: {e}")
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                decoded_message = message.decode()

                # Check if the client is new and requesting to set a username
                if addr not in self.username:
                    if decoded_message.startswith("USERNAME_CHECK:"):
                        username = decoded_message.split(":")[1].strip()

                        # Check if the username is unique
                        if username in self.username.values():
                            # Notify the client that the username is taken
                            self.server_socket.sendto("USERNAME_TAKEN".encode(), addr)
                        else:
                            # Add the username and notify the client that it's accepted
                            self.username[addr] = username
                            self.clients.append(addr)
                            self.server_socket.sendto("USERNAME_ACCEPTED".encode(), addr)
                            print(f"New client connected: {addr} with username: {username}")
                    continue  # Skip further processing until the username is confirmed

                # Normal message handling (after username is set)
                print(f"Received message from {addr} ({self.username[addr]}): {decoded_message}")
                self.messages.put((f"{self.username[addr]}: {decoded_message}".encode(), addr))

            except Exception as e:
                print(f"Error receiving message: {e}")

    def broadcast(self):
        """Broadcast messages to all connected clients."""
        while True:
            while not self.messages.empty():
                message, addr = self.messages.get()
                for client in self.clients:
                    if client != addr:  # Avoid sending the message back to the sender
                        try:
                            self.server_socket.sendto(message, client)
                        except Exception as e:
                            print(f"Error sending to {client}: {e}")
                            self.clients.remove(client)  # Remove the client if an error occurs

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
