
import socket
import threading
import time
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

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(f"Received: {message.decode('utf-8')}")
        except :
            break

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


# Memulai thread untuk menerima pesan dari server
t = threading.Thread(target=receive, daemon=True)  # Set daemon=True agar thread mati saat program selesai
t.start()

# Beri jeda agar thread penerima siap
time.sleep(1)

try:
    signup_message = f"SIGNUP_TAG: {name}"
    client.sendto(signup_message.encode('utf-8'), (ipaddr, port))
    print(f"{signup_message}")  # Debug log
except Exception as e:
    print(f"Error sending signup message: {e}")

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



# Loop untuk mengirimkan pesan
while True:
    message = input("")
    if message == "!q":
        print("Exiting chat...")
        break  # Keluar dari loop jika pengguna mengetik !q
    try:
        full_message = f"{name}: {message}"
        client.sendto(full_message.encode('utf-8'), (ipaddr, port))
        print(f"Sent: {full_message}")  # Debug log
    except Exception as e:
        print(f"Error sending message: {e}")

client.close()
print("Connection closed.")