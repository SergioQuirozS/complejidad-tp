class Griddle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.used = None
        self.down = None
        self.right = None