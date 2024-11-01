import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from queue import Queue

class ChatNode:
    DEFAULT_PORT = 8083

    def __init__(self):
        print("Loading Kegeprek Chat App")
        self.local_address = ("0.0.0.0", self.DEFAULT_PORT)
        self.remote_address = None
        self.nickname = ""
        self.password = "kegeprek"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unique_name_confirmed = False
        self.message_queue = Queue()

        
        self.root = tk.Tk()
        self.get_connection_details()
        self.root.title("Kegeprek Chat App")
        self.setup_nickname_frame()
        self.setup_chat_frame()

        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.after(100, self.process_incoming_messages)
        print("Inisialisasi Berhasil")
    def is_port_available(self, ip, port):
        """Cek apakah IP and port bisa tersedia."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                test_socket.bind((ip, port))
                return True
            except OSError:
                return False
    def validate_port(self, port):
        """Memvalidasi port number."""
        return 0 <= port <= 65535
    def validate_ip(self, ip):
        """Memvalidasi format IP address."""
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
    def get_connection_details(self):
        """Minta pengguna untuk memasukkan IP, port, password, dan nama, dengan opsi mengulangi jika terjadi kesalahan."""
        print("Mengambil detail koneksi..")
        while True:
            local_ip = simpledialog.askstring("Connection Setup", "Masukan lokal IP address (default: 0.0.0.0):", parent=self.root) or "0.0.0.0"
            if local_ip is None:
                self.root.quit()
                return
            if self.validate_ip(local_ip):
                break
            else:
                messagebox.showerror("Invalid Local IP", "Lokal IP address tidak valid. Masukan IP address yang valid.")
        while True:
            local_port = simpledialog.askinteger("Connection Setup", "Masukkan local port :", parent=self.root) or 0
            if local_port is None:
                self.root.quit()
                return
            if self.validate_port(local_port):
                if self.is_port_available(local_ip, local_port):
                    break
                else:
                    messagebox.showerror("Port Unavailable", f"The IP address and port {local_ip}:{local_port} are not available. Please choose a different IP or port.")
            else:
                messagebox.showerror("Invalid Local Port", "local port tidak valid. Range port number 0 - 65535.")

        while True:
            remote_ip = simpledialog.askstring("Connection Setup", "Masukkan remote IP address :", parent=self.root)
            if remote_ip is None:
                self.root.quit()
                return
            if self.validate_ip(remote_ip):
                break
            else:
                messagebox.showerror("Remote IP Tidak Valid", "Remote IP address tifak valid.")

        while True:
            remote_port = simpledialog.askinteger("Connection Setup", "Masukkan remote port (default: 8083):", parent=self.root) or 8083
            if remote_port is None:
                self.root.quit()
                return
            if self.validate_port(remote_port):
                break
            else:
                messagebox.showerror("Remote Port Tidak Valid", "Remote port number tidak valid. Range port number 0 - 65535.")
        try:
            self.local_address = (local_ip, local_port)
            self.remote_address = (remote_ip, remote_port)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.local_address)
            print(f"Klien terhubung ke port lokal  {self.socket.getsockname()[1]}")
            messagebox.showinfo("Berhasil terkoneksi", f"Klien terhubung ke port lokal  {self.socket.getsockname()[1]}")
        except socket.error as e:
            messagebox.showerror("Kesalahan Binding", f"Gagal mengikat ke {local_ip}:{local_port}. Error: {e}")
            self.root.quit()

        while True:
            password = simpledialog.askstring("Password", "Masukkan password:", parent=self.root, show="*")
            if password is None:
                self.root.quit()
                return
            if password == self.password:
                break
            else:
                messagebox.showerror("Password Salah", "Password salah. Coba ulang lagi.")
        messagebox.showinfo("Berhasil terkoneksi", f"Klien terhubung ke port lokal {self.socket.getsockname()[1]}")

    def setup_nickname_frame(self):
        """Bikin frame untuk input nama panggilan."""
        self.nickname_frame = tk.Frame(self.root)
        self.nickname_frame.pack(fill="both", expand=True)

        tk.Label(self.nickname_frame, text="Masukkan nama anda:").pack(pady=10)
        self.nickname_entry = tk.Entry(self.nickname_frame)
        self.nickname_entry.pack(pady=5)
        tk.Button(self.nickname_frame, text="Submit", command=self.submit_nickname).pack(pady=10)
        self.nickname_entry.bind("<Return>", lambda event: self.submit_nickname())

    def setup_chat_frame(self):
        """Bikin frame untuk chat interface."""
        self.chat_frame = tk.Frame(self.root)

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state='disabled')
        self.text_area.pack(padx=10, pady=5, expand=True, fill='both')

        self.msg_entry = tk.Entry(self.chat_frame, width=50)
        self.msg_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill='x')
        self.msg_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=5, side=tk.RIGHT)

    def submit_nickname(self):
        """Handle nickname submission."""
        self.nickname = self.nickname_entry.get().strip()
        if not self.nickname:
            messagebox.showerror("Dibutuhkan nama", "Anda harus memasukkan nama untuk login.")
        else:
            print(f"Mengirim nama '{self.nickname}' ke server untuk verivikasi.")
            self.check_username()

    def receive_messages(self):
        """Menunggu pesan masuk and tambahkan ke antrian."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()

                if decoded_message == "NAMA_SUDAH_TERPAKAI":
                    self.unique_name_confirmed = False
                    self.message_queue.put("Nama sudah terpakai. Masukkan nama lain.")
                    print("Received 'NAMA_SUDAH_TERPAKAI' from server. Meminta nama baru.")
                    messagebox.showerror("Nama sudah terpakai", "Pilih nama baru untuk masuk ke chat.")

                elif decoded_message == "NAMA_DITERIMA":
                    self.unique_name_confirmed = True
                    self.message_queue.put("Nama diterima. Anda sudah bisa mengirim pesan.")
                    print("Received 'NAMA_DITERIMA' from server. Nama terkonfirmasi")
                    messagebox.showinfo("Sukses", "Nama diterima! Anda sudah bisa mengirim pesan.")
                    self.transition_to_chat()
                elif self.unique_name_confirmed:
                    self.message_queue.put(decoded_message)
            except Exception as e:
                self.message_queue.put(f"Error : {e}")
                messagebox.showerror(f"Ada error di: {e}")
                break

    def check_username(self):
        """Mengirim permintaan pengecekan nama pengguna ke server."""
        if self.remote_address:
            self.socket.sendto(f"CEK_NAMA: {self.nickname}".encode(), self.remote_address)
            print(f"Cek nama '{self.nickname}' dengan server.")
        else:
            print("Kesalahan: Alamat remote tidak diatur dengan benar")


    def transition_to_chat(self):
        """Transition the GUI from nickname input to chat interface."""
        self.nickname_frame.pack_forget()
        self.chat_frame.pack(fill="both", expand=True)
        self.root.title(f"Kegeprek Chat App - {self.nickname}")
        print("Transitioned to chat mode.")

    def display_message(self, message):
        """Display a message in the text area."""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')
        print(f"Displayed message: {message}")

    def send_message(self, event=None):
        """Send the message typed in the entry field to the remote node."""
        if self.unique_name_confirmed:
            message = self.msg_entry.get().strip()
            if message:
                try:
                    self.socket.sendto(message.encode(), self.remote_address)
                    self.display_message(f"You: {message}")
                    self.msg_entry.delete(0, tk.END)
                except Exception as e:
                    self.display_message(f"Error : {e}")

    def process_incoming_messages(self):
        """Process messages from the queue and display them in the GUI."""
        while not self.message_queue.empty():
            message = self.message_queue.get()
            print(f"Processing message from queue: {message}")
            self.display_message(message)
        self.root.after(100, self.process_incoming_messages)

if __name__ == "__main__":
    chat_node = ChatNode()
    chat_node.root.mainloop()


