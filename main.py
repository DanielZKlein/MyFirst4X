import sys, pygame
import pygame.gfxdraw
import pygame.freetype

pygame.init()

from pygame.locals import *
from math import *

size = width, height = 1600, 800
black = 0, 0, 0
white = 255, 255, 255
myfont10 = pygame.font.SysFont('arial', 10)
myfont14 = pygame.font.SysFont('arial', 14)

map_dict = {}
screen = pygame.display.set_mode(size)

class HexCell:
    def __init__(self, row_col, terrain = "grass", features = [], resources = []):
        self.row_col = row_col
        self.cube = self.row_col.to_cube()
        self.terrain = terrain
        self.features = features
        self.resources = resources
        master_render_list.append(self)
        (x, y) = self.row_col.to_screen_coords()
        self.debug_box = textBox(x+25, y+50)
        self.debug_box.setText(self.row_col.to_str())
        self.debug_box.disable()

    def __repr__(self):
        return "HexCell(%s)" % self.row_col.to_str()
    def render(self):
        (hexrect.x, hexrect.y) = self.row_col.to_screen_coords()
        screen.blit(hex, hexrect)

class row_col_coords:
    def __init__(self, row=0, col=0):
        self.col = int(col)
        self.row = int(row)
    def to_cube(self):
        x = self.col - (self.row - (self.row&1)) / 2
        z = self.row
        y = -x-z
        return cube_coords(x, y, z)
    def to_str(self):
        readable = "Row/Col: " + str(self.row) + ", " + str(self.col)
        return (readable)
    def to_screen_coords(self, offsetx=0, offsety=0):
        screenY = floor(hex_height * 0.75) * self.row
        screenX = hex_width * self.col
        if self.row&1 == 1:
            screenX += floor(hex_width/2)
        return (screenX, screenY)

class cube_coords:
    def __init__(self, x=0, y=0, z=0):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def to_row_col(self):
        col = self.x + (self.z - (self.z&1)) / 2
        row = self.z
        return row_col_coords(col, row)
    def to_str(self):
        readable = "Cube: " + str(self.x) + ", " + str(self.y) + ", " + str(self.z)
        return (readable)

class textBox:
    def __init__(self, x=0, y=0, size=10):
        self.x = x
        self.y = y
        self.text = ""
        if size == 14:
            self.myFont = myfont14
        else:
            self.myFont = myfont10
        master_render_list.append(self)
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def setText(self, text):
        self.text = text

    def render(self):
        if self.enabled == True:
            tempSurface = self.myFont.render(self.text, False, black)
            screen.blit(tempSurface, (self.x, self.y))

def myPixelToHex(x, y):
    # first, find row. Should be straightforward.
    row = floor(y / (hex_height * 0.75))
    # okay, we have the row. If we're in an odd row, calculate the offset
    if row&1 == 1:
        x -= floor(hex_width/2)
    # cool, now just get me the lowest col number in this range
    col = floor(x / hex_width)
    # note this function doesn't work super well around the point top and bottom parts of the hexes, but whatev
    return row, col

def hex_round(cube):
    rx = round(cube.x)
    ry = round(cube.y)
    rz = round(cube.z)

    dx = abs(rx-cube.x)
    dy = abs(ry-cube.y)
    dz = abs(rz-cube.z)

    if dx > dy and dx > dz:
        rx = -ry-rz
    elif dy > dz:
        ry = -rx-rz
    else:
        rz = -rx-ry

    return cube_coords(rx, ry, rz)



# load graphics
hex = pygame.image.load("hex63.png")
hexrect = hex.get_rect()

# set globals
hex_width = hexrect.width
hex_height = hexrect.height
horizontal_iterations = floor(width / hex_width)
vertical_iterations = floor(height / (hex_height * 0.75))
cur_offset = (0, 0)  # for scrolling the map -- not yet implemented

# create master list of render objects
master_render_list = []

# create grid
for row in range(0, vertical_iterations):
    for col in range(0, horizontal_iterations):
        this_cell = HexCell(row_col_coords(row, col))
        map_dict[(row, col)] = this_cell

def render_all():
    for thing in master_render_list:
        thing.render()

mousePosDebug = textBox(x=1, y=1, size=14)
last_highlit_cell = -1

while 1:
    hexrect.x = 0
    hexrect.y = 0
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit()
        if event.type == MOUSEMOTION:
            mousePosDebug.setText(str(event.pos))
            (x, y) = event.pos
            (row, col) = myPixelToHex(x, y)
            row = min(vertical_iterations, row)
            col = min(horizontal_iterations, col)
            row = max(0, row)
            col = max(0, col)
            hover_cell = map_dict[(row, col)]
            hover_cell.debug_box.enable()
            if last_highlit_cell != hover_cell and last_highlit_cell != -1:
                last_highlit_cell.debug_box.disable()
            last_highlit_cell = hover_cell
    screen.fill(white)
    render_all()
    pygame.display.flip()
