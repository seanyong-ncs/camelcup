from PIL import Image, ImageOps

screen_h, screen_w = 112, 160
tile_h, tile_w = 16, 32
camel_h = 16
offset = 1

canvas = Image.new("RGBA", (screen_w, screen_h), (228, 210, 170))
tile = Image.open("graphics/tilealt.png")

def tile_iso(i, j):
    x = i*0.5*tile_w + j*-0.5*tile_w + (screen_w/2 - tile_w/2)
    y = i*0.5*tile_h + j*0.5*tile_h + tile_h*1.5 + offset
    return (round(x), round(y))

def iso_camel(i, j, k=0):
    x = i*0.5*tile_w + j*-0.5*tile_w + (screen_w/2 - tile_w/4)
    y = i*0.5*tile_h + j*0.5*tile_h + tile_h*1.25 - k*camel_h/2.75 + offset
    return (round(x), round(y))

def iso_mod(i, j, k=0):
    x = i*0.5*tile_w + j*-0.5*tile_w + (screen_w/2 - tile_w/4)
    y = i*0.5*tile_h + j*0.5*tile_h + tile_h*1.7 + offset
    return (round(x), round(y))

def pos_to_iso(pos): 
    if pos == -1:
        return (2, -1)
    if pos < 4:
        return pos, 0
    elif pos < 8:
        return 4, pos - 4
    elif pos < 12:
        return (12 - pos), 4
    elif pos < 16:
        return 0, (16 - pos)

def draw_board(tile):
    for i in range(5):
        canvas.alpha_composite(tile, tile_iso(i, 0))
    for i in range(1, 4):
        canvas.alpha_composite(tile, tile_iso(0, i))
    for i in range(1, 4):
        canvas.alpha_composite(tile, tile_iso(4, i))
    for i in range(5):
        canvas.alpha_composite(tile, tile_iso(i, 4))

def draw_camel(color, pos, height=0):
    if pos != 0:
        pos = (pos + 1) % 16 # Offset starting position
    
    flip = "_flip" if pos >= 8 else ""
    camel_sprite = Image.open(f"graphics/camel16x16_{color}.png")
    i, j = pos_to_iso(pos)
    if (pos >= 0 and pos < 4) or pos >= 12:
        canvas.alpha_composite(ImageOps.mirror(camel_sprite), iso_camel(i, j, height))
    else:
        canvas.alpha_composite(camel_sprite, iso_camel(i, j, height))

def draw_mod(mod_type, pos):
    if pos != 0:
        pos = (pos + 1) % 16 # Offset starting position
    orientation = "_up" if pos >= 8 else "_down" 
    mod_sprite = Image.open(f"graphics/{mod_type}{orientation}_16x16.png")
    width, height = mod_sprite.size

    scale_factor = 1
    mod_sprite = mod_sprite.resize((round(width * scale_factor), round(height * scale_factor)), resample=Image.Resampling.BOX)
    i, j = pos_to_iso(pos)

    if (pos >= 0 and pos < 4) or pos >= 12:
        mod_sprite = ImageOps.mirror(mod_sprite)
        
    canvas.alpha_composite(mod_sprite, iso_mod(i, j, 0))


draw_board(tile)


draw_camel("blue", 14, 2)

draw_camel("green", 14, 1)
draw_camel("yellow", 14, 0 )

draw_camel("white", 16, 1)
draw_camel("orange", 16)

draw_mod("boost", 15)
draw_mod("boost", 13)
draw_mod("boost", 1)

# for i in range(16):
#     draw_mod("boost", i)

sf = 4
canvas = canvas.resize((screen_w * sf, screen_h * sf), resample=Image.Resampling.BOX)

canvas.show()