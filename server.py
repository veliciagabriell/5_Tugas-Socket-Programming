import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("192.168.0.135", 8081))

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
                message_decoded = message.decode()  # Decode once
                print(message_decoded)
                
                if addr not in clients:
                    clients.append(addr)

                for client in clients:
                    try:
                        if message_decoded.startswith("SIGNUP_TAG: "):
                            name = message_decoded.split(": ")[1]
                            server.sendto(f"{name} joined!".encode(), client)
                        else:
                            server.sendto(message, client)
                    except:
                        clients.remove(client)
            except UnicodeDecodeError:
                pass  # Handle decoding issues silently

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

t1.join()
t2.join()