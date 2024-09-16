#!/usr/bin/python3

import discord
from discord.ext import commands

import cor

class BetterTransitBot(commands.Bot):

    meeting_cache = []

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    def add_meeting(self, m):
        self.meeting_cache.insert(0, m)
        print(f'Added meeting: {m}')

if __name__ == '__main__':

    # Get secret token from file
    token = ''
    with open('token.txt', 'r') as f:
        token = f.readline()

    # Create and run bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = BetterTransitBot(command_prefix='!', intents=intents)
    #client.run(token)

    # Initialize meetings
    client.add_meeting(cor.get_meeting())
