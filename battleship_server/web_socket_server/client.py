import asyncio
import threading
import websockets


class Client:
    def __init__(self, web_socket, event_loop, client_id):
        self.id = client_id
        self.__message_received = None
        self.__web_socket = web_socket
        self.__event_loop = event_loop

    def on_message_received(self, message_received_handler):
        self.__message_received = message_received_handler

    async def receive_messages(self):
        async for message in self.__web_socket:
            if self.__message_received:
                thread = threading.Thread(target=self.__message_received, args=(self.id, message), daemon=True)
                thread.start()

    def close(self):
        asyncio.ensure_future(self.__web_socket.close(), loop=self.__event_loop)

    def send_message(self, message):
        try:
            asyncio.ensure_future(self.__web_socket.send(message), loop=self.__event_loop)
        except websockets.exceptions.ConnectionClosedOK:
            pass
