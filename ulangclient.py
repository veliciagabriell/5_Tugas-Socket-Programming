import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

class ChatNode:
    def __init__(self, local_host="0.0.0.0", local_port=8081, remote_host="192.168.0.135", remote_port=8081, nickname=""):
        self.local_address = (local_host, local_port)
        self.remote_address = (remote_host, remote_port)
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.local_address)
        self.unique_name_confirmed = False

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname", parent = msg)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target = self.gui_loop)
        receive_thread = threading.Thread(target = self.receive)

        gui_thread.start()
        receive_thread.start()
    
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightpink")

        self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightpink")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightpink")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)
        
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font = ("Arial",12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()


    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.socket.send(message.encode())
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.socket.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.socket.recvfrom(4096)
                if message == 'NICK':
                    self.socket.send(self.nickname.encode())
                else:
                    if self.gui_done:
                        self.text_area.config(state = 'normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end') 
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError: 
                break
            except:
                print("Error")
                self.socket.close()
                break


    def receive_messages(self):
        """Listen for incoming messages and print them."""
        while True:
            try:
                message, address = self.socket.recvfrom(4096)
                decoded_message = message.decode()
                if decoded_message == "USERNAME_TAKEN":
                    print("\nNickname is already taken. Please choose a new one.")
                    self.unique_name_confirmed = False
                    self.request_new_nickname()
                elif decoded_message == "USERNAME_ACCEPTED":
                    print("\nNickname accepted. You can start chatting.")
                    self.unique_name_confirmed = True
                elif self.unique_name_confirmed:
                    # Move the cursor up, print the message, then move the cursor back down
                    print(f"\r{decoded_message}\nYou: ", end="")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        """Send messages to the remote node."""
        while True:
            if self.unique_name_confirmed:
                message = input("You: ")
                try:   
                    full_message = f"{message}"
                    self.socket.sendto(full_message.encode(), self.remote_address)
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break

    def request_new_nickname(self):
            """Request the user to input a new nickname if the current one is taken."""
            while not self.unique_name_confirmed:
                self.nickname = input("Enter a new nickname: ")
                self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
                break

    def start(self):
        """Start the chat node."""
        # Send initial name for checking
        self.socket.sendto(f"USERNAME_CHECK: {self.nickname}".encode(), self.remote_address)
        # Start a separate thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        # Handle sending messages in the main thread
        self.send_messages()

if __name__ == "__main__":
    local_host = input("Enter your local IP address (default is 0.0.0.0): ") or "0.0.0.0"
    local_port = int(input("Enter your local port (default is 8081): ") or 8081)
    remote_host = input("Enter the remote IP address to connect to: ")
    remote_port = int(input("Enter the remote port (default is 8081): ") or 8081)

    password =  input("Enter password: ")
    while password != "lahkocak":
        print("Wrong password.")
        password =  input("Enter password: ")

    client = ChatNode(local_host, local_port, remote_host, remote_port, nickname="")
    nickname = input("Enter your nickname: ")