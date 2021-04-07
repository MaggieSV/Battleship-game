import asyncio
import threading
import websockets

from .client import Client


class WebSocketServer:
    def __init__(self, port):
        self.__port = port
        self.__server_is_running = False
        self.__event_loop = None
        self.__current_client_id = 0
        self.__client_connected = None
        self.__client_disconnected = None
        self.__message_received = None
        self.__clients = {}
        self.__clients_lock = threading.Lock()

    def on_client_connected(self, client_connected_handler):
        self.__client_connected = client_connected_handler

    def on_client_disconnected(self, client_disconnected_handler):
        self.__client_disconnected = client_disconnected_handler

    def on_message_received(self, message_received_handler):
        self.__message_received = message_received_handler

        with self.__clients_lock:
            for id, client in self.__clients.items():
                client.on_message_received(message_received_handler)

    def run(self):
        thread = threading.Thread(target=self.__run_websocket_server, daemon=True)
        thread.start()
        return thread

    def stop(self):
        self.__server_is_running = False

    def disconnect_client(self, client_id):
        client = self.__get_client(client_id)

        if client:
            client.close()

    def send_message(self, client_id, message):
        client = self.__get_client(client_id)

        if client:
            client.send_message(message)

    def __run_websocket_server(self):
        self.__server_is_running = True

        self.__event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__event_loop)

        start_server = websockets.serve(self.__client_connection, port=self.__port, close_timeout=1)

        self.__event_loop.run_until_complete(start_server)
        self.__event_loop.run_until_complete(self.__wait_for_server_to_stop())
        self.__disconnect_clients()

        tasks = asyncio.all_tasks(self.__event_loop)
        for task in tasks:
            task.cancel()
            try:
                self.__event_loop.run_until_complete(task)
            except asyncio.CancelledError:
                pass

    async def __client_connection(self, web_socket, path):
        client = Client(web_socket, self.__event_loop, self.__generate_client_id())
        client.on_message_received(self.__message_received)
        self.__add_client(client, path)

        try:
            await client.receive_messages()
        except websockets.exceptions.ConnectionClosedError:
            pass
        finally:
            self.__remove_client(client)

    async def __wait_for_server_to_stop(self):
        while self.__server_is_running:
            await asyncio.sleep(0.1)

    def __disconnect_clients(self):
        temporary_clients = {}

        with self.__clients_lock:
            for id, client in self.__clients.items():
                temporary_clients[id] = client

        for id, client in temporary_clients.items():
            client.close()

    def __generate_client_id(self):
        client_id = self.__current_client_id
        self.__current_client_id += 1
        return client_id

    def __add_client(self, client, path):
        with self.__clients_lock:
            self.__clients[client.id] = client

        if self.__client_connected:
            thread = threading.Thread(target=self.__client_connected, args=(client.id, path), daemon=True)
            thread.start()

    def __remove_client(self, client):
        with self.__clients_lock:
            del self.__clients[client.id]

        if self.__client_disconnected:
            thread = threading.Thread(target=self.__client_disconnected, args=(client.id,), daemon=True)
            thread.start()

    def __get_client(self, client_id):
        client = None

        with self.__clients_lock:
            client = self.__clients.get(client_id)

        return client
