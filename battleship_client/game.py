import re
from threading import Lock

class Game:
    def __init__(self, screen):
        self.screen = screen

    def set_map_size(self, map_size):
        self.map_size = map_size

    def make_plan(self, plan):
        self.you_map = plan['yourGrid']
        self.opp_map = plan['opponentGrid']

    def print_plan(self):
        self.screen.print_plan(self.map_size, self.you_map, self.opp_map)

    def your_move(self):
        self.flush_input()
        letter, number = None, None
        while letter is None or number is None:
            try:
                shot = input("\n      Your shot: ")
            except EOFError: pass
            if 1 < len(shot) < 5:
                x, y = self.check_shot(shot)
                letter, number = x, y
        return (x, y)
    
    def check_shot(self, shot):
        x, y = None, None
        c = re.findall("[a-zA-Z]+", shot)
        if len(c)==1 and len(c[0])==1:
            letter = c[0].upper()
            if 65 <= ord(letter) < (65+self.map_size):
                x = ord(letter) - 65
        d = re.findall(r"\d+", shot)
        # print(c, d)
        if len(d)==1:
            number = int(d[0])
            if 0 < number <= (0+self.map_size):
                y = number-1
        # print(x, y)
        return x, y

    def flush_input(self):
        try:
            # Windows
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            # Unix
            import sys, termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
