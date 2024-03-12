#!/usr/bin/python3

import discord
from discord.ext import commands

import cor

class BetterTransitBot(commands.Bot):

    meetings = []

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

if __name__ == '__main__':

    # Get secret token from file
    token = ''
    with open('token.txt', 'r') as f:
        token = f.readline()

    # Create and run bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = BetterTransitBot(command_prefix='!', intents=intents)
    # client.run(token)

    m = cor.getMeeting() 
