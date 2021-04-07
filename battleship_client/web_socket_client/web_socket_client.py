import asyncio
import threading
import websockets


class WebSocketClient:
    def __init__(self):
        self.__uri = None
        self.__client_is_running = False
        self.__event_loop = None
        self.__web_socket = None
        self.__connected = None
        self.__disconnected = None
        self.__error_received = None
        self.__message_received = None
        self.__message_threads = []

    # get your function and do it when client connect to server
    def on_connected(self, connected_handler):
        self.__connected = connected_handler

    # get your function and do it when client disconnect from server
    def on_disconnected(self, disconnected_handler):
        self.__disconnected = disconnected_handler

    def on_error(self, error_handler):
        self.__error_received = error_handler

    def on_message_received(self, message_received_handler):
        self.__message_received = message_received_handler

    # get uri and connect client to server
    def connect(self, uri):
        self.__uri = uri
        thread = threading.Thread(target=self.__run_websocket_client, daemon=True)
        thread.start()
        return thread

    def disconnect(self):
        self.__client_is_running = False

    def send_message(self, message):
        if self.__web_socket:
            asyncio.ensure_future(self.__web_socket.send(message), loop=self.__event_loop)

    def __run_websocket_client(self):
        self.__event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__event_loop)
        self.__event_loop.run_until_complete(self.__receive_messages_from_server())

    async def __receive_messages_from_server(self):
        try:
            async with websockets.connect(self.__uri) as web_socket:
                self.__web_socket = web_socket
                self.__client_is_running = True

                if self.__connected:
                    thread = threading.Thread(target=self.__connected, daemon=True)
                    self.__message_threads.append(thread)
                    thread.start()

                while self.__client_is_running:
                    try:
                        message = await asyncio.wait_for(web_socket.recv(), timeout=0.1)

                        if self.__message_received:
                            thread = threading.Thread(target=self.__message_received, args=(message,), daemon=True)
                            self.__message_threads.append(thread)
                            thread.start()
                    except asyncio.TimeoutError:
                        pass

                self.__send_disconnected()
        except websockets.exceptions.ConnectionClosedOK:
            self.__send_disconnected()
        except websockets.exceptions.WebSocketException as exception:
            self.__send_error(exception)
            self.__send_disconnected()
        except OSError as exception:
            self.__send_error(exception)

        for thread in self.__message_threads:
            thread.join()
        self.__message_threads = []

    def __send_disconnected(self):
        self.__web_socket = None

        if self.__disconnected:
            thread = threading.Thread(target=self.__disconnected, daemon=True)
            self.__message_threads.append(thread)
            thread.start()

    def __send_error(self, error):
        self.__web_socket = None

        if self.__error_received:
            thread = threading.Thread(target=self.__error_received, args=(error,), daemon=True)
            self.__message_threads.append(thread)
            thread.start()
