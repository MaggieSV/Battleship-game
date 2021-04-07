import copy
import random
from .battleship_ship import Ship
from .battleship_field import Field
    
class Map:
    """
    1. run_starter() try to set the ships on the map 
    2. set_ships() create list of ships
    3. random_ship() try to create a new ship
    4. find_new_field() try to set a new field on the ship
    """

    def __init__(self, map_size):
        self.map_size = map_size
        self.map = [[Field(x,y) for x in range(map_size)]
                                for y in range(map_size)]
        self.fields_map = [(x,y) for x in range(map_size) for y in range(map_size)]
        # print(self.fields_map)

    def __repr__(self):
        view = '\n'.join(str([str(f) for f in line]) for line in self.map)
        return f"\n{view}\n"

    def __str__(self):
        letters = "   ".join(chr(c) for c in range(65, 65+self.map_size))
        # numbers = "   ".join(str(n) for n in range(self.map_size))
        first = "\n{0:<8}{1}".format(' ', letters)
        separator = "\n{0:<6}{1}".format(' ',"---".join("+"*(self.map_size+1)))
        view = first + separator
        for i,row in enumerate(self.map, 0):
            next_row = "\n{:>5} | {} |".format (i," | ".join(str(f) for f in row))
            view += next_row + separator
        return view

    def run_starter(self):
        for i in range(1000):
            if self.set_ships():
                break
        else: print(f"Setting of ships is impossible")
        self.game_over = False

    def set_ships(self):
        self.ships = list()
        ships_number = 5
        area = self.create_area(range(self.map_size), range(self.map_size))
        self.clean_area(area)
        for i,size in enumerate(range(ships_number,0,-1), 1):
            for x in range(i):
                ship = self.random_ship(size)
                if ship:
                    self.draw_ship(ship)
                    self.ships.append(ship)
                else:
                    return False
        self.change_states('.', ' ', area)
        return True

    def random_ship(self, size):
        fields_map = list(self.fields_map)
        while fields_map:
            field = random.choice(fields_map)
            x,y = field
            if self.map[y][x].check_value() == 'empty':
                new_ship = Ship(field)
                for s in range(size-1):
                    new_field = self.find_new_field(new_ship)
                    if new_field:
                        new_ship.add_field(new_field)
                    else:
                        new_ship = False
                        break
                if new_ship:
                    new_ship.set_sank()
                    return new_ship
            fields_map.remove(field)
        return False

    def find_new_field(self, the_ship):
        ship_fields = list(the_ship.fields)
        while ship_fields:
            ship_field = random.choice(ship_fields)
            x,y = ship_field
            four_fields = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            while four_fields:
                new_field = random.choice(four_fields)
                x,y = new_field
                if 0 <= x < self.map_size and 0 <= y < self.map_size:
                    check = self.map[y][x].check_value()
                    if new_field not in the_ship.fields and check == 'empty':
                        return new_field
                four_fields.remove(new_field)
            ship_fields.remove(ship_field)
        return False

    def change_states(self, old_state, new_state, area):
        for x,y in area:
            if 0 <= x < self.map_size and 0 <= y < self.map_size:
                self.map[y][x].change_value(old_state, new_state)

    def check_sank_ship(self, field):
        for ship in self.ships:
            if ship.check_field(field):
                if ship.decrease_sank():
                    self.sank_ship(ship)
                    self.ships.remove(ship)
                    if not self.ships:
                        self.game_over = True

    def clean_area(self, area):
        self.create_states(' ', area)

    def create_area(self, xx, yy): #range(xx), range(yy)
        return [(x,y) for x in xx for y in yy]

    def create_states(self, new_state, area):
        for x,y in area:
            if 0 <= x < self.map_size and 0 <= y < self.map_size:
                self.map[y][x].set_new_value(new_state)

    def draw_ship(self,ship):
        for field in ship.fields:
            self.draw_ship_around(field)
        self.create_states('O', ship.fields)

    def draw_ship_around(self, field):
        x,y = field
        area = self.create_area(range(x-1,x+2), range(y-1,y+2))
        self.create_states('.', area)        

    def sank_ship(self, ship):
        for field in ship.fields:
            self.draw_ship_around(field)
        self.create_states('#', ship.fields)


    def check_change_state(self, x, y):
        field = self.map[y][x]
        value = field.check_value()
        if value == "empty":
            field.change_value(' ', '.')
        elif value == "occupied":
            field.change_value('O', 'X')
            self.check_sank_ship((x,y))
        return field.check_value()

    def json_show_map(self):
        json_map = [[str(f) for f in line] for line in self.map]
        return json_map
    
    def json_hide_map(self, game_over):
        if not game_over:
            json_map = [[f.hide_value() for f in line] for line in self.map]
        else:
            json_map = [[str(f) for f in line] for line in self.map]
        return json_map

    def show_ships(self):
        print(str(self))


if __name__ == "__main__":
    for i in range(100):
        mapa = Map(10)
        mapa.run_starter()