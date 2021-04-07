class Ship:
    def __init__(self, field):
        self.fields = [field]
    
    def __str__(self):
        return str(self.fields)
    
    def add_field(self, new_field):
        self.fields.append(new_field)
    
    def check_field(self, field):
        if field in self.fields:
            return True
        return False

    def size(self):
        return len(self.fields)
    
    def decrease_sank(self):
        self.sank -= 1
        if self.sank == 0:
            return True
        return False

    def set_sank(self):
        self.sank = len(self.fields)