from json import dumps, loads
from battleship_game import Plan

class Game:
    def __init__(self, server, clients):
        self.server = server
        self.server.on_message_received(self.receive_message)
        self.id = {"p1" : clients[0], "p2" : clients[1]}
        self.plan = Plan(self.id["p1"], self.id["p2"])
        self.map = {"p1" : self.plan.player["p1"]["map"],
                    "p2" : self.plan.player["p2"]["map"] }

    def start(self):
        self.map_size = Plan.map_size
        self.server.send_message(self.id["p1"], dumps({"id": "MapSize", "data": self.map_size}) )
        self.server.send_message(self.id["p2"], dumps({"id": "MapSize", "data": self.map_size}) )
        self.continue_game("p1", "p2")

    def fresh_screen(self, player1, player2, game_over=False):
        self.send_map(self.id[player1], self.map[player1], self.map[player2], game_over)
        self.send_map(self.id[player2], self.map[player2], self.map[player1], game_over)

    def continue_game(self, player1, player2):
        self.fresh_screen(player1, player2)
        self.send_message(player1, player2, "move")

    def stop_game(self, player1, player2):
        self.fresh_screen(player1, player2, game_over=True)
        self.send_message(player1, player2, "game over") # you lose, you win
        self.server.disconnect_client(self.id[player1])
        self.server.disconnect_client(self.id[player2])

    def stop_continue_game(self, player1, player2):
        if self.plan.check_game_over(player1):
            self.stop_game(player1, player2)
        else:
            self.continue_game(player1, player2)

    def send_map(self, p_id, player_map, opponent_map, game_over):
        self.server.send_message(p_id, dumps({"id": "Map",
                                              "data": {"yourGrid": player_map.json_show_map(),
                                                       "opponentGrid": opponent_map.json_hide_map(game_over)} }))

    def send_message(self, player, opponent, mess, x=None, y=None):
        dump_mess = {"player": {"move": {"id": "YourMove"},
                                "game over": {"id": "YouLose"},
                                "miss": {"id": "YouMissed", "data": {"x": x, "y": y}},
                                "hit": {"id": "YouHitShip", "data": {"x": x, "y": y}},
                                "sank": {"id": "YouSankShip","data": {"x": x, "y": y}} },
                     "opponent": {"move": {"id": "OpponentMove"},
                                  "game over": {"id": "YouWin"},
                                  "miss": {"id": "OpponentMissed", "data": {"x": x, "y": y}},
                                  "hit": {"id": "OpponentHitShip", "data": {"x": x, "y": y}},
                                  "sank": {"id": "OpponentSankShip", "data": {"x": x,"y": y}} }}
        self.server.send_message(self.id[player], dumps(dump_mess["player"][mess]))
        self.server.send_message(self.id[opponent], dumps(dump_mess["opponent"][mess]))

    def receive_message(self, player1, message):
        shot = loads(message)
        x, y = shot["data"]['x'], shot["data"]['y']
        if player1 == self.id["p1"]:
            player1 = "p1"; player2 = "p2"
        else: player1 = "p2"; player2 = "p1"
        field_state = self.plan.shoot_field(player2, x, y)
        self.send_message(player1, player2, field_state, x, y)
        self.stop_continue_game(player2, player1) # turn players
