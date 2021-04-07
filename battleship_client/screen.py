from colorama import Back, Fore, Style
from json import loads
import os
TAB = f"{'':6}"

class Screen:
    def __init__(self):
        self.message_color = Fore.YELLOW
        self.stop_color = Style.RESET_ALL
        self.information_under_map = str()
        self.info_message = {'CannotConnectBecauseOtherPlayersAreConnected' : self.cannot_connect,
                             'OpponentConnected' : self.opponent_connected,
                             'OpponentDisconnected' : self.opponent_disconnected,
                             'OpponentMove' : self.opponent_move,
                             'WaitingForOpponent' : self.wait_for_opponent,
                             'WinWalkover' : self.win_walkover,
                             'YourMove' : self.your_move, }

    def clear_screen(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("      __  __ _____    __ __       __")
        print("     / _)/_/ /  / /  /_ (_  /_ ///_/")
        print("    /__)/ / /  / /_ /__ __)/  ///\n")

    def handle_message(self, id):
        self.info_message[id]()

    def print_message(self, info):
        print(f"\n{self.message_color}{info}{self.stop_color}")

    def cannot_connect(self):
        self.print_message("Cannot connect because other players are connected")

    def opponent_connected(self):
        self.print_message("Opponent connected")

    def opponent_disconnected(self):
        self.print_message("Opponent disconnected")
    
    def opponent_move(self):
        self.print_message(f"{TAB}Opponent move")

    def set_opponent_info(self, info, x, y):
        x, y = chr(x+65), y+1
        self.information_under_map = f"{'':6}{Fore.CYAN}{info}{x}{y}{Style.RESET_ALL}"

    def set_opponent_hit_ship(self, x, y):
        self.set_opponent_info("Opponent hit ship: ", x, y)

    def set_opponent_missed(self, x, y):
        self.set_opponent_info("Opponent missed: ", x, y)

    def set_opponent_sank_ship(self, x, y):
        self.set_opponent_info("Opponent sank ship: ", x, y)

    def wait_for_opponent(self):
        self.print_message("Waiting for opponent...")
    
    def win_walkover(self):
        self.print_message("You win a walkover")

    def set_you_info(self, info, x, y):
        tab = f"{'':{len(self.letters)+16}}"
        x, y = chr(x+65), y+1
        self.information_under_map = f"{tab}{Fore.CYAN}{info}{x}{y}{Style.RESET_ALL}"

    def set_you_hit_ship(self, x, y):
        self.set_you_info("You hit ship: ", x, y)

    def set_you_missed(self, x, y):
        self.set_you_info("You missed: ", x, y)

    def set_you_sank_ship(self, x, y):
        self.set_you_info("You sank ship: ", x, y)

    def you_lose(self):
        you_lose = f"{Back.RED}{Fore.BLACK}{'YOU LOSE!':^30}{Style.RESET_ALL}"
        print(f"\n{TAB}{Fore.RED}{'GAME OVER':^30}{Style.RESET_ALL}")
        print(f"{TAB}{you_lose}")

    def you_win(self):
        you_win = f"{Back.GREEN}{Fore.BLACK}{'YOU WIN!':^30}{Style.RESET_ALL}"
        print(f"\n{TAB}{Fore.GREEN}{'GAME OVER':^30}{Style.RESET_ALL}")
        print(f"{TAB}{you_win}")
    
    def your_move(self):
        self.print_message("Your move")

    def print_plan(self, map_size, y_map, o_map):
        self.print_header()
        self.letters = "   ".join(chr(c) for c in range(65, 65+map_size))
        format_letters = "\n{0:8}{1}{0:10}{1}".format('', self.letters)
        header = "\n{0:6}{1:^{3}}{0:6}{2:^{3}}".format('','YOUR SHIPS','ENEMY SHIPS',len(self.letters)+4)
        separator = "{0:6}{1}{0:6}{1}".format('',"---".join("+"*(map_size+1) ) )
        print(f"{header}\n{format_letters}\n{separator}")
        for y in range(map_size):
            player1 = "{:5} | {} |".format(y+1," | ".join(y_map[y]) )
            player2 = "{:5} | {} |".format(y+1," | ".join(o_map[y]) )
            print(f"{player1}{player2}\n{separator}")
        print(self.information_under_map)
        