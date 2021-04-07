from json import loads, dumps
from threading import Lock
from time import sleep
from game import Game
from screen import Screen
# import re

class MessageService:
    def __init__(self, websocket_client):
        self.screen = Screen()
        self.game = Game(self.screen)
        self.lock = Lock()
        self.websocket_client = websocket_client
        self.message_service = {'CannotConnectBecauseOtherPlayersAreConnected' : self.print_message,
                                'OpponentConnected' : self.print_message,
                                'OpponentDisconnected' : self.print_message,
                                'OpponentMove' : self.opponent_move,
                                'OpponentHitShip' : self.opponent_hit_ship,
                                'OpponentMissed' : self.opponent_missed,
                                'OpponentSankShip' : self.opponent_sank_ship,
                                'WaitingForOpponent' : self.print_message,
                                'WinWalkover' : self.print_message,
                                'YourMove' : self.your_move,
                                'YouHitShip' : self.you_hit_ship,
                                'YouMissed' : self.you_missed,
                                'YouSankShip' : self.you_sank_ship,
                                'YouLose' : self.you_lose,
                                'YouWin' : self.you_win,
                                'MapSize' : self.set_map_size,
                                'Map' : self.set_plan }

    def convert_message(self, message):
        with self.lock:
            self.message = loads(message)
            self.message_id = self.message['id']
            # print("***Convert message***", self.message_id)
            self.message_service[self.message_id]()

    def print_message(self):
        # with self.lock:
        self.screen.handle_message(self.message_id)

    def set_map_size(self):
        # print("Jestem w set_map_size")
        self.game.set_map_size(self.message['data'])

    def set_plan(self):
        # print("Jestem w set_plan")
        plan = self.message['data']
        self.game.make_plan(plan)

    def opponent_move(self):
        # print("Jestem w opponent_move")
        self.game.print_plan()
        self.print_message()

    def opponent_hit_ship(self):
        shot = self.message['data']
        self.screen.set_opponent_hit_ship(shot['x'], shot['y'])

    def opponent_missed(self):
        # print("Jestem w opp_missed")
        shot = self.message['data']
        self.screen.set_opponent_missed(shot['x'], shot['y'])

    def opponent_sank_ship(self):
        shot = self.message['data']
        self.screen.set_opponent_sank_ship(shot['x'], shot['y'])

    def your_move(self):
        # print("Jestem w your_move")
        self.game.print_plan()
        x, y = self.game.your_move()
        self.websocket_client.send_message(dumps({'id' : "Shot", 'data' : {'x': x, 'y': y} }))

    def you_hit_ship(self):
        shot = self.message['data']
        self.screen.set_you_hit_ship(shot['x'], shot['y'])

    def you_missed(self):
        shot = self.message['data']
        self.screen.set_you_missed(shot['x'], shot['y'])

    def you_sank_ship(self):
        shot = self.message['data']
        self.screen.set_you_sank_ship(shot['x'], shot['y'])

    def you_lose(self):
        self.game.print_plan()
        self.screen.you_lose()

    def you_win(self):
        self.game.print_plan()
        self.screen.you_win()
