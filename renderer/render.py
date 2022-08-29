import pygame
import sys


pygame.init()
screen_h = 700
screen_w = 1100
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Camel Cup Renderer")
clock = pygame.time.Clock()

tile_surface = pygame.image.load('graphics/floor_compact.png')
tile_rect = tile_surface.get_rect(midbottom= (80, 300))

bg_surface = pygame.Surface((screen_w, screen_h))
bg_surface.fill("#222034")


tile_h = 105
tile_w = 192
camel_h = 96

def tile_iso(i, j):
    x = i*0.52*tile_w + j*-0.52*tile_w + (screen_w/2 - tile_w/2)
    y = i*0.48*tile_h + j*0.48*tile_h + tile_h*1.5
    return (x, y)

def iso_camel(i, j, k=0):
    x = i*0.52*tile_w + j*-0.52*tile_w + (screen_w/2 - tile_w/4)
    y = i*0.48*tile_h + j*0.48*tile_h + tile_h*1.25 - k*camel_h/2
    return (x, y)

def draw_board():
    tile_surface = pygame.image.load('graphics/floor_compact.png')
    for i in range(5):
        screen.blit(tile_surface, tile_iso(i, 0))
    for i in range(1, 4):
        screen.blit(tile_surface, tile_iso(0, i))
    for i in range(1, 4):
        screen.blit(tile_surface, tile_iso(4, i))
    for i in range(5):
        screen.blit(tile_surface, tile_iso(i, 4))

def pos_to_iso(pos):
    if pos < 4:
        return pos, 0
    elif pos < 8:
        return 4, pos - 4
    elif pos < 12:
        return (12 - pos), 4
    elif pos < 16:
        return 0, (16 - pos)

def draw_camel(color, pos, height=0):
    flip = "_flip" if pos >= 8 else ""
    camel = pygame.image.load(f"graphics/camel_{color}{flip}.png")
    i, j = pos_to_iso(pos)
    if pos < 4 or pos >= 12:
        screen.blit(pygame.transform.flip(camel, True, False), iso_camel(i, j, height))
    else:
        screen.blit(camel, iso_camel(i, j, height))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface, (0,0))
    # screen.blit(tile_surface, (0,0))
    draw_board()
    draw_camel("yellow", 7, 0)
    draw_camel("orange", 2, 0)
    draw_camel("blue", 10, 0)
    draw_camel("white", 15, 0)
    draw_camel("green", 15, 1)
    draw_camel("orange", 15, 2)
    draw_camel("blue", 15, 3)
    pygame.display.update()
    clock.tick(60)