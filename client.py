import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from queue import Queue

class ChatNode:
    def __init__(self):
        # Initialize variables for connection details
        self.local_address = ("0.0.0.0", 8081)  # Default values
        self.remote_address = ("", 8081)
        self.nickname = ""
        self.password = "lahkocak"  # Expected password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unique_name_confirmed = False
        self.message_queue = Queue()  # Queue for storing messages

        # Initialize the GUI
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window initially

        # Get connection details from the user
        self.get_connection_details()

        # Show the main window once connection details are set
        self.root.deiconify()
        self.root.title("Chatroom")

        # Messages display area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.text_area.pack(padx=10, pady=5, expand=True, fill='both')

        # Message entry field
        self.msg_entry = tk.Entry(self.root, width=50)
        self.msg_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill='x')
        self.msg_entry.bind("<Return>", self.send_message)

        # Send button
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=5, side=tk.RIGHT)

        # Start GUI update loop
        self.root.after(100, self.process_incoming_messages)

    def get_connection_details(self):
        """Prompt the user for IP, port, password, and nickname."""
        local_ip = simpledialog.askstring("Connection Setup", "Enter your local IP address (default is 0.0.0.0):", parent=self.root) or "0.0.0.0"
        local_port = simpledialog.askinteger("Connection Setup", "Enter your local port (default is 8081):", parent=self.root) or 8081
        remote_ip = simpledialog.askstring("Connection Setup", "Enter the remote IP address to connect to:", parent=self.root)
        remote_port = simpledialog.askinteger("Connection Setup", "Enter the remote port (default is 8081):", parent=self.root) or 8081

        while True:
            password = simpledialog.askstring("Password", "Enter password:", parent=self.root, show="*")
            if password == self.password:
                break
            else:
                messagebox.showerror("Incorrect Password", "The password is incorrect. Please try again.")

        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.root)
        if not self.nickname:
            messagebox.showerror("Nickname Required", "You need a nickname to join the chat.")
            self.root.quit()

        self.local_address = (local_ip, local_port)
        self.remote_address = (remote_ip, remote_port)
        self.socket.bind(self.local_address)

        # Check username
        self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)

    def display_message(self, message):
        """Display a message in the text area."""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def receive_messages(self):
        """Listen for incoming messages and add them to the queue."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()
                
                if decoded_message == "USERNAME_TAKEN":
                    self.unique_name_confirmed = False
                    self.message_queue.put("Nickname already taken. Enter a new nickname.")
                    self.request_new_nickname()
                elif decoded_message == "USERNAME_ACCEPTED":
                    self.message_queue.put("Nickname accepted. You can start chatting.")
                    self.unique_name_confirmed = True
                elif self.unique_name_confirmed:
                    self.message_queue.put(decoded_message)
            except Exception as e:
                self.message_queue.put(f"Error receiving message: {e}")
                break

    def send_message(self, event=None):
        """Send the message typed in the entry field to the remote node."""
        if self.unique_name_confirmed:
            message = self.msg_entry.get()
            if message:
                try:
                    self.socket.sendto(message.encode(), self.remote_address)
                    self.display_message(f"You: {message}")
                    self.msg_entry.delete(0, tk.END)
                except Exception as e:
                    self.display_message(f"Error sending message: {e}")

    def _prompt_for_nickname(self):
        while not self.unique_name_confirmed:
            new_nickname = simpledialog.askstring("Nickname Taken", "Enter a new nickname:", parent=self.root)
            
            # Cek apakah pengguna membatalkan dialog atau memberikan nickname kosong
            if not new_nickname:
                messagebox.showinfo("Exit", "You need a valid nickname to join the chat.")
                self.root.quit()
                return  # Keluar dari fungsi jika nickname tidak valid
            
            # Kirim permintaan username baru ke server
            self.nickname = new_nickname
            self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)

    def request_new_nickname(self):
        while not self.unique_name_confirmed:
            new_nickname = simpledialog.askstring("Nickname Taken", "Enter a new nickname:", parent=self.root)
            if new_nickname:
                self.nickname = new_nickname
                self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)  # Pastikan ini benar
                break
            else:
                messagebox.showinfo("Exit", "You need a valid nickname to join the chat.")
                self.root.quit()

    def process_incoming_messages(self):
        """Process messages from the queue and display them in the GUI."""
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.display_message(message)
        self.root.after(100, self.process_incoming_messages)  # Schedule the next call

    def start(self):
        """Start the chat node and the GUI."""
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    chat_node = ChatNode()
    chat_node.start()



