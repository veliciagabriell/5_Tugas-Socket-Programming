
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
            print(message.decode('utf-8'))
        except :
            break


# Memulai thread untuk menerima pesan dari server
t = threading.Thread(target=receive, daemon=True)  # Set daemon=True agar thread mati saat program selesai
t.start()


try:
    signup_message = f"SIGNUP_TAG: {name}"
    client.sendto(signup_message.encode('utf-8'), (ipaddr, port))
    print(f"{signup_message}")  # Debug log
except Exception as e:
    print(f"Error sending signup message: {e}")



# Loop untuk mengirimkan pesan
while True:
    message = input("")
    if message == "!q":
        print("Exiting chat...")
        break  # Keluar dari loop jika pengguna mengetik !q
    try:
        full_message = message
        client.sendto(full_message.encode('utf-8'), (ipaddr, port))
    except Exception as e:
        print(f"Error sending message: {e}")

client.close()
print("Connection closed.")