import socket
import threading
import queue

messages = queue.Queue()
clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.0.135", 8081))
print("Server is running...")

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))


        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            try:
                message_decoded = message.decode('utf-8')  # Decode once
                print(f"Received from {addr}: {message_decoded}")
                
                if message_decoded.startswith("SIGNUP_TAG: "):
                    name = message_decoded.split(": ")[1]
                    clients[addr] = name  # Add the client to the list
                    join_message = f"{name} joined the chat!"
                    print(join_message)  # Debug log
                    # Broadcast the join message to all clients
                    for client in clients:
                        server.sendto(join_message.encode('utf-8'), client)
                else:
                    # Regular chat message; prepend the sender's name
                    sender_name = clients.get(addr, "Unknown")
                    full_message = f"{sender_name}: {message_decoded}"
                    print(f"Broadcasting: {full_message}")

                    # Send the message to all connected clients
                    for client in clients:
                        try:
                            server.sendto(full_message.encode('utf-8'), client)
                        except Exception as e:
                            print(f"Error sending to {client}: {e}")
                           
            except UnicodeDecodeError:
                print("Failed to decode message, skipping...")

# Start the receive and broadcast threads
t1 = threading.Thread(target=receive, daemon=True)
t2 = threading.Thread(target=broadcast, daemon=True)

t1.start()
t2.start()

t1.join()
t2.join()