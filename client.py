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
# import tkinter as tk

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ambil IP address dan port dari input pengguna
ipaddr = input("IP Address: ")
port = int(input("Port: "))  # Convert port to int

pw = input("Insert password: ") #masukkan password

while (pw != "roomchat"):
    print("Wrong password")
    pw = input("Insert password: ")

name = input("Nickname: ")

ack_receive = {}
def receive():
    global ack_received
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print (message.decode())

            # #memisahkan nomor urut (seq number) dari pesan utama
            # #TCP over UDP melihat urutan
            # seq_num, msg = decoded_message.split(' ', 1)
            # seq_num = int(seq_num)

            # #send ACK ke sender
            # ack_message = f"ACK {seq_num}"
            # client.sendto(ack_message.encode('utf-8'),_)

            # # If the message is not a duplicate, display it
            # if seq_num not in ack_received:
            #     chat_listbox.insert(tk.END, msg)
            #     ack_received[seq_num] = True


        except:
            pass

# Memulai thread untuk menerima pesan dari server
t = threading.Thread(target=receive)
t.start()

# def send (sock, ipaddr, port, msg_entry, username, seq_num):
#     msg = f" {seq_num} {username}: {msg_entry.get()}"

#     sock.sendto(message.encode('utf-8'), (ipaddr, port))

#     while True:
#         try:
#             ack, _ = sock.recvform(1024)
#             ack_message = ack.decode('utf-8')
#             ack_num = int(ack_message.split(' '[1]))

#             if ack_num==seq_num:
#                 print(f"ACK {ack_num} received")
#                 break
#         except:
#             print("Resending message...")
#             sock.sendto(message.encode('utf-8')), (ipaddr,port)


# Mengirimkan pesan signup dengan nama pengguna
client.sendto(f"SIGNUP_TAG: {name}".encode(), (ipaddr, port))

# Loop untuk mengirimkan pesan
while True:
    message = input("")
    if message == "!q":
        break  # Keluar dari loop jika pengguna mengetik !q
    else:
        client.sendto(f"{name}: {message}".encode(), (ipaddr, port))
