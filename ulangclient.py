# import socket
# import threading
# import tkinter
# import tkinter.scrolledtext
# from tkinter import simpledialog

# class ChatNode:
#     def __init__(self, local_host="0.0.0.0", local_port=8081, remote_host="192.168.0.123", remote_port=8081, nickname=""):
#         self.local_address = (local_host, local_port)
#         self.remote_address = (remote_host, remote_port)
#         self.nickname = nickname
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind(self.local_address)
#         self.unique_name_confirmed = False

#     #     msg = tkinter.Tk()
#     #     msg.withdraw()

#     #     self.nickname = simpledialog.askstring("Nickname", "Enter your nickname", parent = msg)
#     #     self.gui_done = False
#     #     self.running = True
#     #     gui_thread = threading.Thread(target = self.gui_loop)
#     #     receive_thread = threading.Thread(target = self.receive_messages)

#     #     gui_thread.start()
#     #     receive_thread.start()
    
#     # def gui_loop(self):
#     #     self.win = tkinter.Tk()
#     #     self.win.configure(bg="lightpink")

#     #     self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightpink")
#     #     self.chat_label.config(font=("Arial", 12))
#     #     self.chat_label.pack(padx=20, pady=5)

#     #     self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
#     #     self.text_area.pack(padx=20, pady=5)
#     #     self.text_area.config(state='disabled')

#     #     self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightpink")
#     #     self.msg_label.config(font=("Arial", 12))
#     #     self.msg_label.pack(padx=20, pady=5)
        
#     #     self.input_area = tkinter.Text(self.win, height=3)
#     #     self.input_area.pack(padx=20, pady=5)

#     #     self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
#     #     self.send_button.config(font = ("Arial",12))
#     #     self.send_button.pack(padx=20, pady=5)

#     #     self.gui_done = True
#     #     self.win.protocol("WM_DELETE_WINDOW", self.stop)
#     #     self.win.mainloop()


#     # def write(self):
#     #     message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
#     #     self.socket.send(message.encode())
#     #     self.input_area.delete('1.0', 'end')

#     # def stop(self):
#     #     self.running = False
#     #     self.win.destroy()
#     #     self.socket.close()
#     #     exit(0)

#     # def receive(self):
#     #     while self.running:
#     #         try:
#     #             message = self.socket.recvfrom(4096)
#     #             if message == 'NICK':
#     #                 self.socket.send(self.nickname.encode())
#     #             else:
#     #                 if self.gui_done:
#     #                     self.text_area.config(state = 'normal')
#     #                     self.text_area.insert('end', message)
#     #                     self.text_area.yview('end') 
#     #                     self.text_area.config(state='disabled')
#     #         except ConnectionAbortedError: 
#     #             break
#     #         except:
#     #             print("Error")
#     #             self.socket.close()
#     #             break


#     # def receive_messages(self):
#     #     """Listen for incoming messages and print them."""
#     #     while True:
#     #         try:
#     #             message, address = self.socket.recvfrom(4096)
#     #             decoded_message = message.decode()
#     #             if decoded_message == "USERNAME_TAKEN":
#     #                 print("\nNickname is already taken. Please choose a new one.")
#     #                 self.unique_name_confirmed = False
#     #                 self.request_new_nickname()
#     #             elif decoded_message == "USERNAME_ACCEPTED":
#     #                 print("\nNickname accepted. You can start chatting.")
#     #                 self.unique_name_confirmed = True
#     #                 # self.text_area.config(state = 'normal')
#     #                 # # self.text_area.insert('end', self.message)
#     #                 # self.text_area.yview('end') 
#     #                 # self.text_area.config(state='disabled')
#     #             elif self.unique_name_confirmed:
#     #                 # Move the cursor up, print the message, then move the cursor back down
#     #                 print(f"\r{decoded_message}\nYou: ", end="")
#     #         except Exception as e:
#     #             print(f"Error receiving message: {e}")
#     #             break

#     # def send_messages(self):
#     #     """Send messages to the remote node."""
#     #     while True:
#     #         if self.unique_name_confirmed:
#     #             message = input("You: ")
#     #             try:   
#     #                 full_message = f"{message}"
#     #                 self.socket.sendto(full_message.encode(), self.remote_address)
#     #             except Exception as e:
#     #                 print(f"Error sending message: {e}")
#     #                 break

#     # def request_new_nickname(self):
#     #         """Request the user to input a new nickname if the current one is taken."""
#     #         while not self.unique_name_confirmed:
#     #             self.nickname = input("Enter a new nickname: ")
#     #             self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
#     #             break

#     # def start(self):
#     #     """Start the chat node."""
#     #     # Send initial name for checking
#     #     self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
#     #     # Start a separate thread for receiving messages
#     #     receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
#     #     receive_thread.start()

#     #     # Handle sending messages in the main thread
#     #     self.send_messages()

#     def receive_messages(self):
#         """Listen for incoming messages and print them."""
#         while True:
#             try:
#                 message, address = self.socket.recvfrom(4096)
#                 decoded_message = message.decode()
#                 if decoded_message == "USERNAME_TAKEN":
#                     print("\nNickname is already taken. Please choose a new one.")
#                     self.unique_name_confirmed = False
#                     self.request_new_nickname()
#                 elif decoded_message == "USERNAME_ACCEPTED":
#                     print("\nNickname accepted. You can start chatting.")
#                     self.unique_name_confirmed = True
#                 elif self.unique_name_confirmed:
#                     # Move the cursor up, print the message, then move the cursor back down
#                     print(f"\r{decoded_message}\nYou: ", end="")
#             except Exception as e:
#                 print(f"Error receiving message: {e}")
#                 break

#     def send_messages(self):
#         """Send messages to the remote node."""
#         while True:
#             if self.unique_name_confirmed:
#                 message = input("You: ")
#                 try:   
#                     full_message = f"{message}"
#                     self.socket.sendto(full_message.encode(), self.remote_address)
#                 except Exception as e:
#                     print(f"Error sending message: {e}")
#                     break

#     def request_new_nickname(self):
#             """Request the user to input a new nickname if the current one is taken."""
#             # while not self.unique_name_confirmed:
#             self.nickname = input("Enter a new nickname: ")
#             self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
#                 # break

#     def start(self):
#         """Start the chat node."""
#         # Send initial name for checking
#         self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
        
#         # Temporarily set unique_name_confirmed to True for testing
#         self.unique_name_confirmed = True

#         # Start a separate thread for receiving messages
#         receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
#         receive_thread.start()

#         # Handle sending messages in the main thread
#         self.send_messages()


# if __name__ == "__main__":
#     local_host = input("Enter your local IP address (default is 0.0.0.0): ") or "0.0.0.0"
#     local_port = int(input("Enter your local port (default is 8081): ") or 8081)
#     remote_host = input("Enter the remote IP address to connect to: ")
#     remote_port = int(input("Enter the remote port (default is 8081): ") or 8081)

#     password =  input("Enter password: ")
#     while password != "lahkocak":
#         print("Wrong password.")
#         password =  input("Enter password: ")

#     # client = ChatNode(local_host, local_port, remote_host, remote_port, nickname="")
#     nickname = input("Enter your nickname: ")

#     chat_node = ChatNode(local_host, local_port, remote_host, remote_port, nickname)
#     chat_node.start()

# import socket
# import threading
# import tkinter
# import tkinter.scrolledtext
# from tkinter import simpledialog

# class ChatNode:
#     def __init__(self, local_host="0.0.0.0", local_port=8081, remote_host="192.168.0.123", remote_port=8081, nickname=""):
#         self.local_address = (local_host, local_port)
#         self.remote_address = (remote_host, remote_port)
#         self.nickname = nickname
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind(self.local_address)
#         self.unique_name_confirmed = False

#         msg = tkinter.Tk()
#         msg.withdraw()

#         self.nickname = simpledialog.askstring("Nickname", "Enter your nickname", parent = msg)
#         self.gui_done = False
#         self.running = True
#         gui_thread = threading.Thread(target = self.gui_loop)
#         receive_thread = threading.Thread(target = self.receive_messages)

#         gui_thread.start()
#         receive_thread.start()
    
#     def gui_loop(self):
#         self.win = tkinter.Tk()
#         self.win.configure(bg="lightpink")

#         self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightpink")
#         self.chat_label.config(font=("Arial", 12))
#         self.chat_label.pack(padx=20, pady=5)

#         self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
#         self.text_area.pack(padx=20, pady=5)
#         self.text_area.config(state='disabled')

#         self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightpink")
#         self.msg_label.config(font=("Arial", 12))
#         self.msg_label.pack(padx=20, pady=5)
        
#         self.input_area = tkinter.Text(self.win, height=3)
#         self.input_area.pack(padx=20, pady=5)

#         self.send_button = tkinter.Button(self.win, text="Send", command=self.send_messages)
#         self.send_button.config(font = ("Arial",12))
#         self.send_button.pack(padx=20, pady=5)

#         self.gui_done = True
#         self.win.mainloop()

#     def receive_messages(self):
#         """Listen for incoming messages and print them."""
#         while True:
#             try:
#                 message, address = self.socket.recvfrom(4096)
#                 decoded_message = message.decode()
#                 if decoded_message == "USERNAME_TAKEN":
#                     self.display_message("Nickname is already taken. Please choose a new one.")
#                     # print("\nNickname is already taken. Please choose a new one.")
#                     self.unique_name_confirmed = False
#                     self.request_new_nickname()
#                 elif decoded_message == "USERNAME_ACCEPTED":
#                     self.display_message("Nickname accepted. You can start chatting.")
#                     # print("\nNickname accepted. You can start chatting.")
#                     self.unique_name_confirmed = True
#                 elif self.unique_name_confirmed:
#                     # Move the cursor up, print the message, then move the cursor back down
#                     # print(f"\r{decoded_message}\nYou: ", end="")
#                     self.display_message(decoded_message)
#             except Exception as e:
#                 print(f"Error receiving message: {e}")
#                 break

#     def send_messages(self):
#         """Send messages to the remote node."""
#         while True:
#             if self.unique_name_confirmed:
#                 # message = input("You: ")
#                 message = self.input_area.get("1.0", 'end').strip()
#                 self.input_area.delete("1.0", 'end')
#                 if message:
#                     full_message = f"{self.nickname}: {message}"  # Format message
#                     self.socket.sendto(full_message.encode(), self.remote_address)  # Send message
#                     self.display_message(full_message)  # Display sent message in chat area

#                 # try:   
#                 #     full_message = f"{message}"
#                 #     self.socket.sendto(full_message.encode(), self.remote_address)
#                 # except Exception as e:
#                 #     print(f"Error sending message: {e}")
#                 #     break

#     def display_message(self, message):
#         """Display message in the text area."""
#         self.text_area.config(state="normal")
#         self.text_area.insert("end", message + "\n")  # Insert message into text area
#         self.text_area.yview("end")  # Scroll to the end of the text area
#         self.text_area.config(state="disabled")  # Disable text area to prevent user editing

#     def request_new_nickname(self):
#             # """Request the user to input a new nickname if the current one is taken."""
#             # while not self.unique_name_confirmed:
#             #     self.nickname = input("Enter a new nickname: ")
#             #     self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
#             #     break
#         """Request the user to input a new nickname if the current one is taken."""
#         new_nickname = simpledialog.askstring("New Nickname", "Enter a new nickname:")
#         if new_nickname:
#             self.nickname = new_nickname
#             self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)

#     def start(self):
#         """Start the chat node."""
#         # Send initial name for checking
#         self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
#         # Start a separate thread for receiving messages
#         receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
#         receive_thread.start()

#         # Handle sending messages in the main thread
#         self.send_messages()


#     def stop(self):
#         """Stop the client."""
#         self.running = False
#         self.win.destroy()
#         self.socket.close()

# if __name__ == "__main__":
#     local_host = input("Enter your local IP address (default is 0.0.0.0): ") or "0.0.0.0"
#     local_port = int(input("Enter your local port (default is 8081): ") or 8081)
#     remote_host = input("Enter the remote IP address to connect to: ")
#     remote_port = int(input("Enter the remote port (default is 8081): ") or 8081)

#     password =  input("Enter password: ")
#     while password != "lahkocak":
#         print("Wrong password.")
#         password =  input("Enter password: ")
    
#     nickname = input("Enter your nickname: ")

#     chat_node = ChatNode(local_host, local_port, remote_host, remote_port, nickname)
#     chat_node.start()

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

class ChatNode:
    def __init__(self):
        # Initialize variables for connection details
        self.local_address = ("0.0.0.0", 8081)  # Default values
        self.remote_address = ("", 8081)
        self.nickname = ""
        self.password = "lahkocak"  # Expected password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.unique_name_confirmed = False

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

    def get_connection_details(self):
        """Prompt the user for IP, port, password, and nickname."""
        # Get Local and Remote IP and Port
        local_ip = simpledialog.askstring("Connection Setup", "Enter your local IP address (default is 0.0.0.0):", parent=self.root) or "0.0.0.0"
        local_port = simpledialog.askinteger("Connection Setup", "Enter your local port (default is 8081):", parent=self.root) or 8081
        remote_ip = simpledialog.askstring("Connection Setup", "Enter the remote IP address to connect to:", parent=self.root)
        remote_port = simpledialog.askinteger("Connection Setup", "Enter the remote port (default is 8081):", parent=self.root) or 8081

        # Validate password
        while True:
            password = simpledialog.askstring("Password", "Enter password:", parent=self.root, show="*")
            if password == self.password:
                break
            else:
                messagebox.showerror("Incorrect Password", "The password is incorrect. Please try again.")

        # Set nickname
        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.root)
        if not self.nickname:
            messagebox.showerror("Nickname Required", "You need a nickname to join the chat.")
            self.root.quit()

        # Set up socket with the provided details
        self.local_address = (local_ip, local_port)
        self.remote_address = (remote_ip, remote_port)
        self.socket.bind(self.local_address)

    def display_message(self, message):
        """Display a message in the text area."""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)  # Auto-scroll to the latest message
        self.text_area.config(state='disabled')

    def receive_messages(self):
        """Listen for incoming messages and display them."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()
                
                if decoded_message == "USERNAME_TAKEN":
                    self.unique_name_confirmed = False
                    self.request_new_nickname()
                elif decoded_message == "USERNAME_ACCEPTED":
                    self.display_message("Nickname accepted. You can start chatting.")
                    self.unique_name_confirmed = True
                elif self.unique_name_confirmed:
                    self.display_message(decoded_message)
            except Exception as e:
                self.display_message(f"Error receiving message: {e}")
                break

    def send_message(self, event=None):
        """Send the message typed in the entry field to the remote node."""
        if self.unique_name_confirmed:
            message = self.msg_entry.get()
            if message:
                try:
                    full_message = f"{message}"
                    self.socket.sendto(full_message.encode(), self.remote_address)
                    self.display_message(f"You: {message}")
                    self.msg_entry.delete(0, tk.END)  # Clear input field
                except Exception as e:
                    self.display_message(f"Error sending message: {e}")

    def request_new_nickname(self):
        """Prompt the user to input a new nickname if the current one is taken."""
        while not self.unique_name_confirmed:
            self.nickname = simpledialog.askstring("Nickname Taken", "Nickname already taken. Enter a new nickname:", parent=self.root)
            if self.nickname:
                self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
            else:
                messagebox.showinfo("Exit", "You need a valid nickname to join the chat.")
                self.root.quit()

    def start(self):
        """Start the chat node and the GUI."""
        self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    chat_node = ChatNode()
    chat_node.start()
