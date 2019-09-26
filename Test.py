import random as rnd
import math as mth
from Data import *
from Griddle import *
from tkinter import *


#Generar datos de entrada
def genItems(num, minWidth, maxWidth, minHeight, maxHeight):
    assert num > 0
    assert maxHeight > minHeight
    assert maxWidth > minWidth
    items = []
    for i in range(num):
        width = rnd.randint(minWidth, maxWidth)
        height = rnd.randint(minHeight, maxHeight)
        item = Item(width,height)
        items.append(item)
    return items


def getSortFun(sortType):
    sortTypes = {}
    sortTypes['width'] = lambda item: -item.w
    sortTypes['height'] = lambda item: -item.h
    sortTypes['area'] = lambda item: -item.w * item.h
    sortTypes['maxside'] = lambda item: -max(item.h, item.w)
    return sortTypes[sortType]


def sortItems(items, sortType):
    sortFunc = getSortFun(sortType)
    items.sort(key=sortFunc)
    return items


class FillGriddle:
    def __init__(self, items):
        assert items
        item = items[0]

        self._root = Griddle(0, 0, item.w, item.h)
        self._items = items
        self._fill(items)

    #Generar Griddle acorde a los items
    def griddleSize(self):
        width = self._root.w
        height = self._root.h

        width = mth.pow(2, int(mth.ceil(mth.log(width, 2))))
        height = mth.pow(2, int(mth.ceil(mth.log(height, 2))))
        return int(width), int(height)

    def _fill(self, items):
        for item in items:
            griddle = self._findGriddle(self._root, item.w, item.h)
            if griddle:
                item.griddle = self._splitGriddle(griddle, item.w, item.h)
            else:
                item.griddle = self._growGriddle(item.w, item.h)

    def _findGriddle(self, griddle, width, height):
        if griddle.used:
            return self._findGriddle(griddle.right, width, height) or self._findGriddle(griddle.down, width, height)
        elif (width <= griddle.w) and (height <= griddle.h):
            return griddle
        else:
            return None

    def _splitGriddle(self, griddle, width, height):
        griddle.used = True
        griddle.down = Griddle(griddle.x, griddle.y + height, griddle.w, griddle.h - height)
        griddle.right = Griddle(griddle.x + width, griddle.y, griddle.w - width, griddle.h)
        return griddle

    def _growGriddle(self, width, height):
        canGrowDown = (width <= self._root.w)
        canGrowRight = (height <= self._root.h)

        shouldGrowRight = canGrowRight and (self._root.h >= (self._root.w + width))
        shouldGrowDown = canGrowDown and (self._root.w >= (self._root.h + height))

        if shouldGrowRight:
            return self._growRight(width, height)
        elif shouldGrowDown:
            return self._growDown(width, height)
        elif canGrowRight:
            return self._growRight(width, height)
        elif canGrowDown:
            return self._growDown(width, height)
        else:
            raise Exception('error')

    def _growRight(self, width, height):
        root = Griddle(0, 0, self._root.w + width, self._root.h)
        root.used = True
        root.down = self._root
        root.right = Griddle(self._root.w, 0, width, self._root.h)

        self._root = root
        griddle = self._findGriddle(self._root, width, height)
        if griddle:
            return self._splitGriddle(griddle, width, height)
        else:
            raise Exception('error')

    def _growDown(self, width, height):
        root = Griddle(0, 0, self._root.w, self._root.h + height)
        root.used = True
        root.down = Griddle(0, self._root.h, self._root.w, height)
        root.right = self._root

        self._root = root
        griddle = self._findGriddle(self._root, width, height)
        if griddle:
            return self._splitGriddle(griddle, width, height)
        else:
            raise Exception('error')


def main():
    #items = genItems(100, 10, 100, 10, 100)
    (width, height, c, items) = getData()
    sortItems(items, 'height')
    fillGriddle = FillGriddle(items)
    #(width, height) = fillGriddle.griddleSize()
    master = Tk()
    canvas = Canvas(master, width=width, height=height, bg='red')

    for item in items:
        griddle = item.griddle
        x, y, width, height = griddle.x, griddle.y, griddle.w, griddle.h
        canvas.create_rectangle(x, y, x + width, y + height, fill='blue')
        canvas.create_text((x, y), text=item.l, anchor='nw', font='40')
    canvas.pack()
    mainloop()


main()


