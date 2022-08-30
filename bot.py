# bot.py
import collections
import os
import sim
import discord
from dotenv import load_dotenv
from models.properties import *
import re
import numpy as np
import copy
from render import render_board

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith("!ev"):
        color_list, pos_dict, mod_dict = parseMessage(message.content)
        render_board(color_list, pos_dict, mod_dict)
        await message.channel.send(file=discord.File('screenshot.jpg'))
        # stack_string, pos_subtitle, move_string = boardDisplay(color_list, pos_dict, mod_dict)
        # await message.channel.send(stack_string)
        # await message.channel.send(pos_subtitle)
        # await message.channel.send(move_string)

        rs = sim.RoundSimulator(color_list, pos_dict, mod_dict)
        probabilities = rs.sim_round()
        evs = rs.calculate_ev()
        embed = create_embed(message, probabilities, evs)
        
        await message.channel.send(embed=embed)

def board_preview(color_list, pos_dict, mod_dict):
    
    max_height = 0

    # Find the maximum height for blank spaces
    for key in pos_dict:
        list_len = len(pos_dict[key])
        if list_len > max_height:
            max_height = list_len
    

    # Construct Emoji based camel stack representation
    all_rows = []
    unified_dict = {**pos_dict,**mod_dict}
    od = collections.OrderedDict(sorted(unified_dict.items()))
    for k, v in od.items():
        v = [v] if not isinstance(v, list) else v
        row = [ColorTile.BLACK for _ in range(max_height - len(v))]
        vr = copy.copy(v)
        vr.reverse()
        row.extend([ColorTile[e.name] for e in vr])
        all_rows.append(row)

    # Transpose 2D list to print vertically
    all_rows_T = np.array(all_rows).T.tolist()

    # Concatinate into a single message
    stack_string = ""
    for row in all_rows_T:
        cur_string = ""
        for element in row:
            cur_string += element.value
        stack_string = stack_string + cur_string + "\n"

    # Add the subtitle for the stack positions
    pos_subtitle = ".     "
    for k, v in od.items():
        pos_subtitle += f"**{k}**         {' ' if k < 9 or k%2 else ''}"

    # Create the section for showing camels that can and cannot move
    
    move_string = '✅ Can Move:       ' + ''.join(f'{ColorTile[c.name].value}' for c in color_list) + '\n' + \
                  "❌ Cannot Move:    " + ''.join(f'{ColorTile[c.name].value}' for c in list(set(color_list) ^ set(Color)))

    return stack_string, pos_subtitle, move_string




def create_embed(message, probabilities, evs):

    # Build embed field message
    def embed_field(p, ev):
        def hl(x): return "__" if x >= 1 else ""
        message = "**Expected Values**\n"
        message += f"{hl(ev[1])}5:           ${ev[1]}{hl(ev[1])}\n"
        message += f"{hl(ev[2])}3:           ${ev[2]}{hl(ev[2])}\n"
        message += f"{hl(ev[3])}2:           ${ev[3]}{hl(ev[3])}\n"
        message += "**Probabilities**\n"
        message += f"1st:        {round(p[1]*100, 2)}%\n"
        message += f"2nd:        {round(p[2]*100, 2)}%\n"
        message += f"3-5th:      {round(p[3]*100, 2)}%\n\n"
        return message

    embed = discord.Embed(title="🐪🏆 EV Results", 
            description=f"Based on the results provided from {message.content}", 
            color=0xffffff)

    emoji_header = ['🥇', '🥈', '🥉', '😞', '😵']

    for p, ev, em in zip(probabilities, evs, emoji_header):
        embed.add_field(name=f"{em} {ColorTile[p[0]].value} {p[0]}", value=f"{embed_field(p, ev)}", inline=True)

    return embed


def parseMessage(message):
    message = message.replace('!ev ', '').lower()

    tokens = message.split(" ")
    tokens.reverse()

    camel_map = {"b": Color.BLUE, "g": Color.GREEN, "o": Color.ORANGE, "y": Color.YELLOW, "w": Color.WHITE}
    tile_map = {"+": TileMod.BOOST, "-": TileMod.TRAP}

    pos_dict = {}
    mod_dict = {}
    color_list = []
    for t in tokens:
        try:
            pos = int(re.findall(r'\d+', t)[0])
            if t[0] in camel_map:
                camel = camel_map[t[0]]
                if t[-1] != 'x':
                    color_list.append(camel)

                if pos in pos_dict:
                    pos_dict[pos].append(camel)
                else:
                    pos_dict[pos] = [camel]
            elif t[0] in tile_map:
                mod_dict[pos] = tile_map[t[0]]
        except:
            print("You mostly likely entered something wrong... please try again")
            return False

    return color_list, pos_dict, mod_dict

client.run(TOKEN)