from Item import *


def getData():
    with open('griddle.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    width = int(content[0].split()[0])
    height = int(content[0].split()[1])
    length = int(content[1])
    data = content[2:]
    items = []
    for i in range(len(data)):
        items.append(Item(int(data[i].split(' ')[1]), int(data[i].split(' ')[2]), data[i].split(' ')[0]))
    return width, height, length, items
