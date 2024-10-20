import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ambil IP address dan port dari input pengguna
try:
    ipaddr = input("IP Address: ")
    port = int(input("Port: "))  # Konversi ke integer
except ValueError:
    print("Invalid input! Port must be a number.")
    exit(1)  # Keluar dengan kode error

pw = input("Insert password: ") #masukkan password

while (pw != "roomchat"):
    print("Wrong password")
    pw = input("Insert password: ")

name = input("Nickname: ")

ack_receive = {}
def receive(sock, chat_listbox):
    global ack_received
    while True:
        try:
            message, _ = client.recvfrom(1024)
            decoded_message = (message.decode())

            #memisahkan nomor urut (seq number) dari pesan utama
            #TCP over UDP melihat urutan
            seq_num, msg = decoded_message.split(' ', 1)
            seq_num = int(seq_num)

            #send ACK ke sender
            ack_message = f"ACK {seq_num}"
            client.sendto(ack_message.encode('utf-8'),_)

        except:
            pass

# Memulai thread untuk menerima pesan dari server
t = threading.Thread(target=receive)
t.start()

def send (sock, ipaddr, port, msg_entry, username, seq_num):
    msg = f" {seq_num} {username}: {msg_entry.get()}"

    sock.sendto(message.encode('utf-8', (ipaddr, port)))

    while True:
        try:
            ack, _ = sock.recvform(1024)
            ack_message = ack.decode('utf-8')
            ack_num = int(ack_message.split(' '[1]))

            if ack_num==seq_num:
                print(f"ACK {ack_num} received")
                break
        except:
            print("Resending message...")
            sock.sendto(message.encode('utf-8')), (ipaddr,port)


# Mengirimkan pesan signup dengan nama pengguna
client.sendto(f"SIGNUP_TAG: {name}".encode(), (ipaddr, port))

# Loop untuk mengirimkan pesan
while True:
    message = input("")
    if message == "!q":
        break  # Keluar dari loop jika pengguna mengetik !q
    else:
        client.sendto(f"{name}: {message}".encode(), (ipaddr, port))
