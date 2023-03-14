import pygame
import json
import time
import os
import random
import threading
from math import *

flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.SCALED
pygame.font.init()
pygame.mixer.init()

# WIDTH, HEIGHT, = 1440, 810
# WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | flags)

WIDTH, HEIGHT, = 960, 540  # DELETE LATER
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16)  # DELETE LATER

pygame.display.set_caption("Grid Sim")

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

COORD_FONT = pygame.font.SysFont('concertone', 25)

BG = pygame.Rect(0, 0, WIDTH, HEIGHT)

FPS = 60

# GRID VARIABLES

X_GRID_COLOR = BLUE
Y_GRID_COLOR = RED
Z_GRID_COLOR = GREEN

y_unit_length = 15
x_unit_length = 20
z_unit_length = 20
width = 16
length = 16
height = 1
x_angle = 120
y_angle = 0
z_angle = y_angle + 90

# y grid variables
y_gap_x_comp = (x_unit_length * cos(radians(y_angle)))  # x-component of red (y) line segment between two blue (x) lines
y_gap_y_comp = (x_unit_length * sin(radians(y_angle)))  # y-component of red (y) line segment between two blue (x) lines
y_magnitude_x_comp = y_gap_x_comp * width  # x-component of entire red line
y_magnitude_y_comp = y_gap_y_comp * width  # y-component of entire red line
y_magnitude = ((y_magnitude_x_comp**2 + y_magnitude_y_comp**2)**0.5)  # length of red line

# x grid variables
x_gap_x_comp = (y_unit_length * cos(radians(x_angle)))  # x-component of blue line segment between two red lines
x_gap_y_comp = (y_unit_length * sin(radians(x_angle)))  # y-component of blue line segment between two red lines
x_magnitude_x_comp = x_gap_x_comp * length  # x-component of entire blue line
x_magnitude_y_comp = x_gap_y_comp * length  # y-component of entire blue line
x_magnitude = ((x_magnitude_x_comp**2 + x_magnitude_y_comp**2)**0.5)  # length of blue line

# z grid variables
z_magnitude = height * z_unit_length  # length of green line

# render lines
grid_origin = (WIDTH // 2), (HEIGHT // 2)

y_center_const = -(x_magnitude_y_comp + y_magnitude_y_comp) // 2  # alters y coordinates of lines to be screen-centered
x_center_const = -(x_magnitude_x_comp + y_magnitude_x_comp) // 2  # alters x coordinates of lines to be screen-centered

# CONTROLS

TERMINAL_SPEED = 1  # in units per frame
GRAVITY = 1.5 / FPS   # in units per frame per frame

# TEXTURES

FOG_WIDTH, FOG_HEIGHT = WIDTH, HEIGHT
FOG_IMAGE = pygame.image.load(r'assets\textures\fog.bmp')
FOG = pygame.transform.scale(FOG_IMAGE, (FOG_WIDTH, FOG_HEIGHT))

BLOCK_WIDTH, BLOCK_HEIGHT = round(x_unit_length - x_gap_x_comp), round(z_unit_length + x_gap_y_comp)

SNOW_TEXTURE = r'assets\textures\snow.bmp'
RETINALLUM_TURF_TEXTURE = r'assets\textures\retinallum_turf.png'
RUSTY_TURF_TEXTURE = r'assets\textures\rustyturf.png'

TEXTURE = [None, SNOW_TEXTURE, RUSTY_TURF_TEXTURE, RETINALLUM_TURF_TEXTURE]
RESISTANCE = [0, 0.9, 1, 1]


# SOUNDS

step_sounds = [pygame.mixer.Sound(r'assets\sounds\step1.wav'), pygame.mixer.Sound(r'assets\sounds\step2.wav')]

place_sound = pygame.mixer.Sound(r'assets\sounds\place.wav')
break_sound = pygame.mixer.Sound(r'assets\sounds\break.wav')

menu_slide_sound = pygame.mixer.Sound(r'assets\sounds\menu_slide.wav')

landing = r'assets\music\landing.wav'
to_the_stars = r'assets\music\to-the-stars.wav'

# WORLD DATA

CHUNKS_FILE = r'assets\world\world_data'

WORLD_FILE = r'assets\world\data.json'

CHUNK_X, CHUNK_Y, CHUNK_Z = 4, 4, 2

WORLD_SIZE_X, WORLD_SIZE_Y, WORLD_SIZE_Z = 64, 64, 16  # total chunks spanning across x axis and y axis of world

WORLD_DIMENSIONS = WORLD_SIZE_X, WORLD_SIZE_Y, WORLD_SIZE_Z

TOTAL_CHUNKS = WORLD_SIZE_Y * WORLD_SIZE_X * WORLD_SIZE_Z  # chunks in world

MAX_COORDS = CHUNK_X * (WORLD_SIZE_X // 2), CHUNK_Y * (WORLD_SIZE_Y // 2), CHUNK_Z * (WORLD_SIZE_Z // 2)

RENDER_DISTANCE = 6  # number of loaded chunks spanning across each direction of player
Z_RENDER_DISTANCE = 4

# PLAYER VARS

SPAWN_POINT = (0, 0, 0)

SPAWN_DIRECTION = 0, 1