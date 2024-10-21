import socket
import threading

class ChatNode:
    def __init__(self, local_host="0.0.0.0", local_port=8081, remote_host="192.168.0.135", remote_port=8081, nickname=""):
        self.local_address = (local_host, local_port)
        self.remote_address = (remote_host, remote_port)
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.local_address)
        self.unique_name_confirmed = False

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
    
    nickname = input("Enter your nickname: ")

    chat_node = ChatNode(local_host, local_port, remote_host, remote_port, nickname)
    chat_node.start()
