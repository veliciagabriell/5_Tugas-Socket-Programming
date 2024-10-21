import socket
import threading
import time

class ChatClient:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.username = None
        self.acknowledged = threading.Event()  # Event for acknowledgment

    def password (self):
        pw = input("Password: ")
        while pw != "roomchat":
            pw = input("Incorrect password. Enter password again: ")

    def send_messages(self):
        """Send messages to the server."""
        self.username = input("Username: ")
        while True:
            message = input(f"{self.username}: ")
            full_message = f"{self.username}: {message}"

            self.acknowledged.clear()  # Reset acknowledgment event
            self.client_socket.sendto(full_message.encode(), self.server_address)

            # Wait for acknowledgment, resend if not received in time
            for _ in range(3):  # Try 3 times
                if not self.acknowledged.wait(2):  # Wait 2 seconds for ACK
                    print("No acknowledgment, resending message...")
                    self.client_socket.sendto(full_message.encode(), self.server_address)
                else:
                    break

    def receive_messages(self):
        """Listen for messages from the server."""
        while True:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                if message:
                    if message.decode() == "ACK":
                        self.acknowledged.set()  # Acknowledgment received
                    else:
                        print(f"\nMessage: {message.decode()}")
            except socket.error as e:
                print(f"Socket error while receiving message: {e}")
            except Exception as e:
                print(f"Error receiving message: {e}")

    def start(self):
        """Start the client."""
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()

if __name__ == "__main__":
    host = "10.5.102.117"  # Server IP
    port = 8081
    client = ChatClient(host, port)
    client.start()
