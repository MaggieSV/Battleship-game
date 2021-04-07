class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = ' '
        self.state = {' ' : "empty",
                      'O' : "occupied",
                      '.' : "miss",
                      'X' : "hit",
                      '#' : "sank"}

    def __str__(self):
        return self.value
        # return str((self.x, self.y))

    def check_value(self):
        return self.state[self.value]

    def change_value(self, old_state, new_state):
        if self.value == old_state: self.value = new_state

    def hide_value(self):
        if self.value == 'O': return ' '
        return self.value

    def set_new_value(self, new_state):
        self.value = new_state