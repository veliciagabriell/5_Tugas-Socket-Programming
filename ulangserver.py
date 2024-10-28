# import socket
# import threading
# import queue

# class ChatServer:
#     def __init__(self, host="192.168.0.123", port=8081):
#         self.server_address = (host, port)
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.server_socket.bind(self.server_address)
#         self.messages = queue.Queue()
#         self.clients = []  # List to keep track of connected clients  
#         self.username = {}
#         print(f"Server is running on {host}:{port}")

#     def receive(self):
#         # """Receive messages from clients."""
#         # while True:
#         #     try:
#         #         message, addr = self.server_socket.recvfrom(1024)
#         #         if addr not in self.clients:
#         #             self.clients.append(addr)  # Add the new client to the list
#         #             print(f"New client connected: {addr}")

#         #         decoded_message = message.decode()
#         #         print(f"Received message from {addr}: {decoded_message}")
#         #         self.messages.put((message, addr))
#         #     except Exception as e:
#         #         print(f"Error receiving message: {e}")
#         while True:
#             try:
#                 message, addr = self.server_socket.recvfrom(1024)
#                 decoded_message = message.decode()

#                 # Check if the client is new and requesting to set a username
#                 if addr not in self.username:
#                     if decoded_message.startswith("USERNAME_CHECK:"):
#                         username = decoded_message.split(":")[1].strip()

#                         # Check if the username is unique
#                         if username in self.username.values():
#                             # Notify the client that the username is taken
#                             self.server_socket.sendto("USERNAME_TAKEN".encode(), addr)
#                         else:
#                             # Add the username and notify the client that it's accepted
#                             self.username[addr] = username
#                             self.clients.append(addr)
#                             self.server_socket.sendto("USERNAME_ACCEPTED".encode(), addr)
#                             print(f"New client connected: {addr} with username: {username}")
#                     continue  # Skip further processing until the username is confirmed

#                 # Normal message handling (after username is set)
#                 print(f"Received message from {addr} ({self.username[addr]}): {decoded_message}")
#                 self.messages.put((f"{self.username[addr]}: {decoded_message}".encode(), addr))

#             except Exception as e:
#                 print(f"Error receiving message: {e}")

#     def broadcast(self):
#         """Broadcast messages to all connected clients."""
#         while True:
#             while not self.messages.empty():
#                 message, addr = self.messages.get()
#                 for client in self.clients:
#                     if client != addr:  # Avoid sending the message back to the sender
#                         try:
#                             self.server_socket.sendto(message, client)
#                         except Exception as e:
#                             print(f"Error sending to {client}: {e}")
#                             self.clients.remove(client)  # Remove the client if an error occurs

#     def start(self):
#         """Start the server threads."""
#         t1 = threading.Thread(target=self.receive, daemon=True)
#         t2 = threading.Thread(target=self.broadcast, daemon=True)

#         t1.start()
#         t2.start()

#         t1.join()
#         t2.join()

# if __name__ == "__main__":
#     chat_server = ChatServer()
#     chat_server.start()

# import socket
# import threading
# import queue
# import tkinter as tk
# import tkinter.scrolledtext as st

# class ChatServer:
#     def __init__(self, host="0.0.0.0", port=8081):
#         self.server_address = (host, port)
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.server_socket.bind(self.server_address)
#         self.messages = queue.Queue()
#         self.clients = []  # List to keep track of connected clients  
#         self.username = {}
#         print(f"Server is running on {host}:{port}")

#         self.root = tk.Tk()
#         self.root.title("Chat Server Log")
#         self.text_area = st.ScrolledText(self.root, state="disabled", width=50, height=20)
#         self.text_area.pack(padx=10, pady=10)
#         self.root.protocol("WM_DELETE_WINDOW", self.stop_server)

#     def log_message(self, message):
#         """Display message in the text area."""
#         self.text_area.config(state="normal")
#         self.text_area.insert("end", message + "\n")
#         self.text_area.yview("end")
#         self.text_area.config(state="disabled")

#     def receive(self):
#         while True:
#             try:
#                 message, addr = self.server_socket.recvfrom(1024)
#                 decoded_message = message.decode()

#                 # Check if the client is new and requesting to set a username
#                 if addr not in self.username:
#                     if decoded_message.startswith("USERNAME_CHECK:"):
#                         username = decoded_message.split(":")[1].strip()

#                         # Check if the username is unique
#                         if username in self.username.values():
#                             # Notify the client that the username is taken
#                             self.server_socket.sendto("USERNAME_TAKEN".encode(), addr)
#                         else:
#                             # Add the username and notify the client that it's accepted
#                             self.username[addr] = username
#                             self.clients.append(addr)
#                             self.server_socket.sendto("USERNAME_ACCEPTED".encode(), addr)
#                             print(f"New client connected: {addr} with username: {username}")
#                     continue  # Skip further processing until the username is confirmed

#                 # Normal message handling (after username is set)
#                 print(f"Received message from {addr} ({self.username[addr]}): {decoded_message}")
#                 self.messages.put((f"{self.username[addr]}: {decoded_message}".encode(), addr))
#                 self.log_message(f"{self.username[addr]}: {decoded_message}")

#             except Exception as e:
#                 print(f"Error receiving message: {e}")
#                 self.log_message(f"Error receiving message: {e}")

#     def broadcast(self):
#         """Broadcast messages to all connected clients."""
#         while True:
#             while not self.messages.empty():
#                 message, addr = self.messages.get()
#                 for client in self.clients:
#                     if client != addr:  # Avoid sending the message back to the sender
#                         try:
#                             self.server_socket.sendto(message, client)
#                         except Exception as e:
#                             print(f"Error sending to {client}: {e}")
#                             self.log_message(f"Error sending to {client}: {e}")
#                             self.clients.remove(client)  # Remove the client if an error occurs


#     def start_server(self):
#         t1 = threading.Thread(target=self.receive, daemon=True)
#         t2 = threading.Thread(target=self.broadcast, daemon=True)

#         t1.start()
#         t2.start()

#         t1.join()
#         t2.join()

#     def stop_server(self):
#         """Stop the server and close the GUI."""
#         self.running = False
#         self.server_socket.close()  # Close the socket
#         self.root.quit()  # Quit the Tkinter loop
#         print("Server stopped.")

# if __name__ == "__main__":
#     chat_server = ChatServer()
#     chat_server.start_server()

import socket
import threading
import queue

class ChatServer:
    def __init__(self, host="0.0.0.0", port=8081):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)
        self.messages = queue.Queue()
        self.clients = []  # Track connected clients
        self.username = {}  # Dictionary to map address to username
        print(f"Server is running on {host}:{port}")

    def receive(self):
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                decoded_message = message.decode()
                print(f"Received message: {decoded_message} from {addr}")  # Tambahkan ini

                # Handle nickname checks
                if addr not in self.username:
                    if decoded_message.startswith("USERNAME_CHECK:"):
                        username = decoded_message.split(":")[1].strip()

                        if username in self.username.values():
                            # Username already taken
                            self.server_socket.sendto("USERNAME_TAKEN".encode(), addr)
                        else:
                            # Username accepted
                            self.username[addr] = username
                            self.clients.append(addr)
                            self.server_socket.sendto("USERNAME_ACCEPTED".encode(), addr)
                            print(f"New client connected: {addr} with username: {username}")
                    continue  # Skip further processing until the username is confirmed

                # Handle regular messages
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
                            self.clients.remove(client)  # Remove client if an error occurs

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
