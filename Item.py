class Item:
    def __init__(self, w, h, l):
        self.w = w
        self.h = h
        self.l = l
        self.griddle = None

    def __str__(self):
        return "Ancho: %d , Alto: %d" % (self.w, self.h)

    def __repr__(self):
        return self.__str__()