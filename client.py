import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from queue import Queue

class ChatNode:
    DEFAULT_PORT = 8083

    def __init__(self):
        print("Loading Kegeprek Chat App...")
        self.local_address = ("0.0.0.0", self.DEFAULT_PORT)
        self.remote_address = None
        self.nickname = ""
        self.password = "kegeprek"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unique_name_confirmed = False
        self.message_queue = Queue()

        self.root = tk.Tk()
        self.root.title("Kegeprek Chat App")

        self.get_connection_details()  
        self.setup_nickname_frame()
        self.setup_chat_frame()

        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.after(100, self.process_incoming_messages)
        print("Loading selesai.")

    def get_connection_details(self):
        """Minta pengguna untuk memasukkan IP, port, password, dan nama, dengan opsi mengulangi jika terjadi kesalahan."""
        print("Mengambil detail koneksi..")
        local_ip = simpledialog.askstring("Connection Setup", "Masukan local IP address (default: 0.0.0.0):", parent=self.root) or "0.0.0.0"
        local_port = simpledialog.askinteger("Connection Setup", "Masukkan local port (leave blank for auto):", parent=self.root) or 0
        remote_ip = simpledialog.askstring("Connection Setup", "Masukkan remote IP address:", parent=self.root)
        remote_port = simpledialog.askinteger("Connection Setup", "Masukkan remote port (default: 8083):", parent=self.root) or 8083

        if not remote_ip:
            messagebox.showerror("Dibutuhkan Remote IP", "Masukkan remotr IP address yang valid.")
            self.root.quit()

        self.local_address = (local_ip, local_port)
        self.remote_address = (remote_ip, remote_port)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.local_address)
        print(f"Klien terhubung ke local port {self.socket.getsockname()[1]}") 

        while True:
            password = simpledialog.askstring("Password", "Masukkan password:", parent=self.root, show="*")
            if password == self.password:
                break
            else:
                messagebox.showerror("Password Salah", "Password salah. Coba lagi.")

    def setup_nickname_frame(self):
        """Persiapan frame untuk input nama."""
        self.nickname_frame = tk.Frame(self.root)
        self.nickname_frame.pack(fill="both", expand=True)

        tk.Label(self.nickname_frame, text="Masukkan nama:").pack(pady=10)
        self.nickname_entry = tk.Entry(self.nickname_frame)
        self.nickname_entry.pack(pady=5)
        tk.Button(self.nickname_frame, text="Kirim", command=self.submit_nickname).pack(pady=10)

    def setup_chat_frame(self):
        """Persiapan tampilan interface."""
        self.chat_frame = tk.Frame(self.root)

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled')
        self.text_area.pack(padx=10, pady=5, expand=True, fill='both')

        self.msg_entry = tk.Entry(self.chat_frame, width=50)
        self.msg_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill='x')
        self.msg_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(self.chat_frame, text="Kirim", command=self.send_message)
        send_button.pack(padx=10, pady=5, side=tk.RIGHT)

    def submit_nickname(self):
        """Menangani nama yang dikirim client."""
        self.nickname = self.nickname_entry.get().strip()
        if not self.nickname:
            messagebox.showerror("Dibutuhkan nama", "Masukkan nama untuk bergabung.")
        else:
            print(f"Mengirim nama '{self.nickname}' ke server untuk diverifikasi.")
            self.check_username()

    def receive_messages(self):
        """Menunggu pesan masuk and tambahkan ke antrian."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()

                if decoded_message == "NAMA_SUDAH_DIPAKAI":
                    self.unique_name_confirmed = False
                    self.message_queue.put("Nama sudah dipakai. Masukkan nama baru")
                    print("Received 'NAMA_SUDAH_TERPAKAI' dari server. Meminta nama baru.")
                elif decoded_message == "NAMA_DITERIMA":
                    self.unique_name_confirmed = True
                    self.message_queue.put("Nama diterima. Anda sudah bisa mengirim pesan.")
                    print("Received 'NAMA_DITERIMA' dari server. Nama terkonfirmasi")
                    
                    self.transition_to_chat()
                elif self.unique_name_confirmed:
                    self.message_queue.put(decoded_message)
            except Exception as e:
                self.message_queue.put(f"Error: {e}")
                break

    def check_username(self):
        """Send the username check request to the server."""
        if self.remote_address:
            self.socket.sendto(f"CEK_NAMA: {self.nickname}".encode(), self.remote_address)
            print(f"Cek nama '{self.nickname}' dengan server.")
        else:
            print("Error: Alamat remote tidak diatur dengan benar")

    def transition_to_chat(self):
        """Alihkan interface dari input nama panggilan ke tampilan obrolan."""
        self.nickname_frame.pack_forget()  
        self.chat_frame.pack(fill="both", expand=True)  
        self.root.title(f"Kegeprek Chat App - {self.nickname}")
        print("Transisi ke chat.")

    def display_message(self, message):
        """Tampilkan pesan di area teks."""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')
        print(f"Tampilan pesan: {message}")

    def send_message(self, event=None):
        "Kirim pesan yang diketik di kolom input ke tujuan."
        if self.unique_name_confirmed:
            message = self.msg_entry.get().strip()
            if message:
                try:
                    self.socket.sendto(message.encode(), self.remote_address)
                    self.display_message(f"Anda: {message}")
                    self.msg_entry.delete(0, tk.END)
                except Exception as e:
                    self.display_message(f"Error: {e}")

    def process_incoming_messages(self):
        "Memproses pesan dari queue dan menampilkannya di GUI."
        while not self.message_queue.empty():
            message = self.message_queue.get()
            print(f"Memproses pesan dari queue: {message}")
            self.display_message(message)
        self.root.after(100, self.process_incoming_messages)

if __name__ == "__main__":
    chat_node = ChatNode()
    chat_node.root.mainloop()     