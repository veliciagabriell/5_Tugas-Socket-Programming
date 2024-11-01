import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from queue import Queue

class ChatNode:
    DEFAULT_PORT = 8083

    def __init__(self):
        print("Initializing ChatNode...")
        self.local_address = ("0.0.0.0", self.DEFAULT_PORT)
        self.remote_address = None  # Will be set in get_connection_details
        self.nickname = ""
        self.password = "kegeprek"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unique_name_confirmed = False
        self.message_queue = Queue()

        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title("Chatroom")
        
        # Get connection details and set up the GUI
        self.get_connection_details()  # Ensure remote address is set correctly here
        self.setup_nickname_frame()
        self.setup_chat_frame()

        # Start background tasks
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.after(100, self.process_incoming_messages)
        print("Initialization complete.")

    def get_connection_details(self):
        """Prompt the user for IP, port, password, and nickname."""
        print("Getting connection details...")
        local_ip = simpledialog.askstring("Connection Setup", "Enter your local IP address (default is 0.0.0.0):", parent=self.root) or "0.0.0.0"
        local_port = simpledialog.askinteger("Connection Setup", "Enter your local port (leave blank for auto):", parent=self.root) or 0
        remote_ip = simpledialog.askstring("Connection Setup", "Enter the remote IP address to connect to:", parent=self.root)
        remote_port = simpledialog.askinteger("Connection Setup", "Enter the remote port (default is 8083):", parent=self.root) or 8083

        if not remote_ip:
            messagebox.showerror("Remote IP Required", "You need to enter a valid remote IP address.")
            self.root.quit()

        self.local_address = (local_ip, local_port)
        self.remote_address = (remote_ip, remote_port)

        # Bind the socket to the local address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.local_address)
        print(f"Client bound to local port {self.socket.getsockname()[1]}")  # Debugging output

        # Prompt for the password
        while True:
            password = simpledialog.askstring("Password", "Enter password:", parent=self.root, show="*")
            if password == self.password:
                break
            else:
                messagebox.showerror("Incorrect Password", "The password is incorrect. Please try again.")

    def setup_nickname_frame(self):
        """Set up the frame for nickname input."""
        self.nickname_frame = tk.Frame(self.root)
        self.nickname_frame.pack(fill="both", expand=True)

        tk.Label(self.nickname_frame, text="Enter your nickname:").pack(pady=10)
        self.nickname_entry = tk.Entry(self.nickname_frame)
        self.nickname_entry.pack(pady=5)
        tk.Button(self.nickname_frame, text="Submit", command=self.submit_nickname).pack(pady=10)

    def setup_chat_frame(self):
        """Set up the frame for the chat interface."""
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
            messagebox.showerror("Nickname Required", "You need a nickname to join the chat.")
        else:
            print(f"Sending nickname '{self.nickname}' to server for verification.")
            self.check_username()

    def receive_messages(self):
        """Listen for incoming messages and add them to the queue."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()

                if decoded_message == "USERNAME_TAKEN":
                    self.unique_name_confirmed = False
                    self.message_queue.put("Nickname already taken. Please enter a new nickname.")
                    print("Received 'USERNAME_TAKEN' from server. Prompting for a new nickname.")
                elif decoded_message == "USERNAME_ACCEPTED":
                    self.unique_name_confirmed = True
                    self.message_queue.put("Nickname accepted. You can start chatting.")
                    print("Received 'USERNAME_ACCEPTED' from server. Nickname confirmed.")
                    
                    self.transition_to_chat()
                elif self.unique_name_confirmed:
                    self.message_queue.put(decoded_message)
            except Exception as e:
                self.message_queue.put(f"Error receiving message: {e}")
                break

    def check_username(self):
        """Send the username check request to the server."""
        if self.remote_address:
            self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
            print(f"Checking username '{self.nickname}' with server.")
        else:
            print("Error: Remote address is not properly set")

    def transition_to_chat(self):
        """Transition the GUI from nickname input to chat interface."""
        self.nickname_frame.pack_forget()  # Hide the nickname input frame
        self.chat_frame.pack(fill="both", expand=True)  # Show the chat interface
        self.root.title(f"Chatroom - {self.nickname}")
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
                    self.display_message(f"Error sending message: {e}")

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