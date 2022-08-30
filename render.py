import collections
import pygame
import sys
from models.properties import *



screen_h = 700
screen_w = 1100

pygame.init()
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Camel Cup Renderer")
clock = pygame.time.Clock()

tile_h = 105
tile_w = 192
camel_h = 96

tile_surface = pygame.image.load('graphics/floor_compact.png')


bg_surface = pygame.Surface((screen_w, screen_h))
bg_surface.fill("#222034")



def tile_iso(i, j):
    x = i*0.52*tile_w + j*-0.52*tile_w + (screen_w/2 - tile_w/2)
    y = i*0.48*tile_h + j*0.48*tile_h + tile_h*1.5
    return (x, y)

def iso_camel(i, j, k=0):
    x = i*0.52*tile_w + j*-0.52*tile_w + (screen_w/2 - tile_w/4)
    y = i*0.48*tile_h + j*0.48*tile_h + tile_h*1.25 - k*camel_h/2
    return (x, y)

def draw_board():
    screen.blit(bg_surface, (0,0))
    for i in range(5):
        screen.blit(tile_surface, tile_iso(i, 0))
    for i in range(1, 4):
        screen.blit(tile_surface, tile_iso(0, i))
    for i in range(1, 4):
        screen.blit(tile_surface, tile_iso(4, i))
    for i in range(5):
        screen.blit(tile_surface, tile_iso(i, 4))



def pos_to_iso(pos): 

    if pos == 0:
        return (2, -1)

    if pos < 4:
        return pos, 0
    elif pos < 8:
        return 4, pos - 4
    elif pos < 12:
        return (12 - pos), 4
    elif pos < 16:
        return 0, (16 - pos)

def draw_camel(color, pos, height=0):
    if pos != 0:
        pos = (pos + 1) % 16 # Offset starting position

    flip = "_flip" if pos >= 8 else ""
    camel = pygame.image.load(f"graphics/camel_{color}{flip}.png")
    i, j = pos_to_iso(pos)
    if (pos > 0 and pos < 4) or pos >= 12:
        screen.blit(pygame.transform.flip(camel, True, False), iso_camel(i, j, height))
    else:
        screen.blit(camel, iso_camel(i, j, height))

def render_board(color_list, pos_dict, mod_dict):
    draw_board()
    od = collections.OrderedDict(sorted(pos_dict.items()))
    for k, v in od.items():
        v = [v] if not isinstance(v, list) else v
        for h, camel in enumerate(v):
            draw_camel(camel.name.lower(), k, h)
    
    pygame.display.update()
    
    pygame.image.save(screen,"screenshot.jpg")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg_surface, (0,0))
        # screen.blit(tile_surface, (0,0))
        draw_board()
        draw_camel("yellow", 7, 0)
        pygame.display.update()
        clock.tick(60)
