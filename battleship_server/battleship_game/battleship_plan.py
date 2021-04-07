# print("file: {}\nname: {}\npackage: {}".format(__file__,__name__,__package__))

from .battleship_map import Map

class Plan:
    map_size = 12

    def __init__(self, p1, p2):
        self.player = {"p1" : {"id":p1, "map":Map(self.map_size)},
                       "p2" : {"id":p2, "map":Map(self.map_size)} }
        self.player["p1"]["map"].run_starter()
        self.player["p2"]["map"].run_starter()

    def make_line_map(self, p, y):
        return "{:>5} | {} |".format (y+1," | ".join(self.player[p]["map"].map[y][x].value for x in range(self.map_size)))

    def show_all(self):
        letters = "   ".join(chr(c) for c in range(65, 65+self.map_size))
        header = "\n{0:<6}{1:^{3}}{0:<6}{2:^{3}}".format(' ','YOUR SHIPS','ENEMY SHIPS',len(letters)+4)
        separator = "{0:<6}{1}{0:<6}{1}".format(' ',"---".join("+"*(self.map_size+1)))
        print(header)
        print("\n{0:<8}{1}{0:<10}{1}".format(' ', letters))
        print(separator)
        for y in range(self.map_size):
            player1 = self.make_line_map("p1", y)
            player2 = self.make_line_map("p2", y)
            print(f"{player1}{player2}\n{separator}")
    
    def shoot_field(self, p, x, y):
        state = self.player[p]["map"].check_change_state(x, y)
        return state

    def check_game_over(self, p):
        return self.player[p]["map"].game_over

if __name__ == '__main__':

    p = Plan()
    p.show_all()
