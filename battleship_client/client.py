from colorama import Fore, Style, init as coloramainit
from web_socket_client import WebSocketClient
from message_service import MessageService
import socket
import websockets

class Client:
    def __init__(self):
        coloramainit()
        self.client = WebSocketClient()
        self.client.on_connected(self.connected)
        self.client.on_disconnected(self.disconnected)
        self.client.on_error(self.error_handler)
        self.client.on_message_received(self.message_handler)
        self.message_service = MessageService(self.client)

    def run(self):
        hostname = input("Server hostname: ")
        # hostname = "localhost"
        if hostname:
            thread_client = self.client.connect(f"ws://{hostname}:17000")
        while thread_client.is_alive():
            try:
                thread_client.join(timeout=0.5)
            except (KeyboardInterrupt, SystemExit):
                self.client.disconnect()
                thread_client.join()

    def connected(self):
        print(f"{Fore.YELLOW}Client connected{Style.RESET_ALL}")

    def disconnected(self):
        print(f"{Fore.YELLOW}Client disconnected{Style.RESET_ALL}")

    def error_handler(self, error):
        print(Fore.RED, end='')
        if isinstance(error, socket.gaierror) or isinstance(error, websockets.exceptions.InvalidURI):
            print("Cannot connect to the server. Verify if the hostname provided is correct.")
        elif isinstance(error, ConnectionRefusedError):
            print("Cannot connect to the server. Verify if the server is running.")
        else:
            print(f"Error received: {error}")
        print(Style.RESET_ALL, end='')

    def message_handler(self, message):
        self.message_service.convert_message(message)

client = Client()
client.run()
input()