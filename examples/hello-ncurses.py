import pyxp
image_layers = pyxp.load("hello.xp")
layer = image_layers[0]
pos = lambda x, y: x + y * layer.height

from curses import wrapper
import _curses
import locale

def main(stdscr):
    locale.setlocale(locale.LC_ALL, '')
    stdscr.clear()    
    for i in range(layer.width):
        for j in range(layer.height):
            tile = layer.tiles[pos(i, j)]
            try:
                char = tile.ascii_code.decode("cp437")
                char = char.replace(chr(0), "")
                stdscr.addstr(i, j, char)
            except _curses.error:
                pass
    
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
