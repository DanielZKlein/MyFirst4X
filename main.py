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
        self.debug_box = textBox(x+10, y+10)
        self.debug_box.setText(str(self.row_col.to_screen_coords()))
        self.debug_box.disable()

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





def render_all():
    for thing in master_render_list:
        thing.render()

mousePosDebug = textBox(x=1, y=1, size=14)
mousePosDebug.disable()

while 1:
    hexrect.x = 0
    hexrect.y = 0
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit()
        if event.type == MOUSEMOTION:
            mousePosDebug.setText(str(event.pos))
    screen.fill(white)
    render_all()
    pygame.display.flip()
