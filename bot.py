# bot.py
import os
import sim
import discord
from dotenv import load_dotenv
from models.properties import *
import re

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
        color_list, pos_dict = parseMessage(message.content)
        mod_dict = {}
        rs = sim.RoundSimulator(color_list, pos_dict, mod_dict)

        probabilities = rs.simulateRound()
        evs = rs.calculateEV()
        await message.channel.send(probabilities)
        await message.channel.send(evs)

def parseMessage(message):
    message = message.replace('!ev ', '')

    tokens = message.split(" ")
    tokens.reverse()

    if len(tokens) != 5:
        print("invalid input")
        return False

    char_mapping = {"b": Color.BLUE, "g": Color.GREEN, "o": Color.ORANGE, "y": Color.YELLOW, "w": Color.WHITE}
    pos_dict = {}
    color_list = []
    for t in tokens:
        try:
            camel = char_mapping[t[0]]
            pos = int(re.findall(r'\d+', t)[0])
            if t[-1] != 'x':
                color_list.append(camel)

            if pos in pos_dict:
                pos_dict[pos].append(camel)
            else:
                pos_dict[pos] = [camel]
            
        except:
            print("You mostly likely entered something wrong... please try again")
            return False

    return color_list, pos_dict

client.run(TOKEN)