import socket
import threading

class ChatClient:
    def __init__(self, host="10.5.102.117", port=8081):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def receive_messages(self):
        """Listen for messages from the server."""
        while True:
            try:
                message, _ = self.client_socket.recvfrom(1024)
                print(f"Message: {message.decode()}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_messages(self):
        """Send messages to the server."""
        while True:
            message = input("You: ")
            self.client_socket.sendto(message.encode(), self.server_address)

    def start(self):
        """Start the client."""
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        self.send_messages()

if __name__ == "__main__":
    host = "10.5.102.117"
    port = 8081
    client = ChatClient(host, port)
    client.start()