from colorama import Fore, Style, init as coloramainit
from json import dumps
from threading import Lock
from web_socket_server import WebSocketServer
from game import Game

coloramainit()
clients = []
clients_lock = Lock()
info_color = Fore.YELLOW
stop_color = Style.RESET_ALL
server = WebSocketServer(17000)

def client_connected(client_id, path):
    print(info_color, f"Client {client_id} connected", stop_color)
    with clients_lock:
        clients.append(client_id)
    if len(clients) == 1:
        server.send_message(client_id, dumps({"id":"WaitingForOpponent"}))
    elif len(clients) == 2:
        server.send_message(clients[0], dumps({"id":"OpponentConnected"}))
        server.send_message(clients[1], dumps({"id":"OpponentConnected"}))
        start_game()
    elif len(clients) > 2:
        server.send_message(client_id, dumps({"id":"CannotConnectBecauseOtherPlayersAreConnected"}))
        server.disconnect_client(client_id)

def client_disconnected(client_id):
    print(info_color, f"Client {client_id} disconnected", stop_color)
    # if clients:
    with clients_lock:
        clients.remove(client_id)
    if len(clients) == 1:
    # if len(clients) == 1 and game.is_ended() == False:
        server.send_message(clients[0], dumps({"id":"OpponentDisconnected"}))
        server.send_message(clients[0], dumps({"id":"WinWalkover"}))
        server.disconnect_client(clients[0])

def start_game():
    game = Game(server, clients)
    game.start()

def start():
    server.on_client_connected(client_connected)
    server.on_client_disconnected(client_disconnected)
    thread = server.run()
    print(info_color, "Server is running", stop_color)

    while thread.is_alive():
        try:
            thread.join(timeout=1)
        except (KeyboardInterrupt, SystemExit):
            server.stop()
            thread.join()

if __name__ == "__main__":
    start()