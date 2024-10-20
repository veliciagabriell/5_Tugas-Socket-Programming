# import socket
# import threading

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# hostname = socket.gethostname()
# IP = socket.gethostbyname(hostname) 
# ipaddr = input("IP Address: ")
# port = input("Port: ")
# name = input ("Nickname: ")
# print(IP)

# def receive():
#     while True:
#         try :
#             message, _ = client.recvfrom(1024)
#             print(message.decode())
#         except:
#             pass

# t = threading.Thread(target=receive)
# t.start()

# client.sendto(f"SIGNUP_TAG:{name}".encode(), ("0.0.0.0", 8081))

# while True :
#     message = input("")
#     if message == "!q":
#         exit()
#     else :
#         client.sendto(f"{name}: {message}".encode(), ("0.0.0.0", 8081) )

import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ambil IP address dan port dari input pengguna
ipaddr = "localhost"
port = int(input("Port: "))  # Convert port to int

pw = input("Insert password: ") #masukkan password


while (pw != "roomchat"):
    print("Wrong password")
    pw = input("Insert password: ")

name = input("Nickname: ")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

# Memulai thread untuk menerima pesan dari server
t = threading.Thread(target=receive)
t.start()

# Mengirimkan pesan signup dengan nama pengguna
client.sendto(f"SIGNUP_TAG: {name}".encode(), (ipaddr, port))

# Loop untuk mengirimkan pesan
while True:
    message = input("")
    if message == "!q":
        break  # Keluar dari loop jika pengguna mengetik !q
    else:
        client.sendto(f"{name}: {message}".encode(), (ipaddr, port))
