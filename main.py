#!/usr/bin/python3

import asyncio
import discord
from discord.ext import commands, tasks

import cor

# TODO:
# - make recent meeting cache
# - make cor meetings cog
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
# - make events cog to update website?

class BetterTransitBot(commands.Bot):

    meeting_cache = []
    target_channel = ''

    async def on_ready(self):
        print(f'Logged on as {self.user}')

        # Get meeting agenda output channel ID
        with open('channel.txt', 'r') as f:
            target_channel = f.readline().strip()
        print(f'Sending meeting agendas to channel ID {target_channel}')

        print(f'Starting update task loop')
        self.update.start()

    @tasks.loop(seconds=5.0)
    async def update(self):
        self.add_meeting(cor.get_recent())

    def add_meeting(self, m):
        """Add a meeting to the meeting cache"""

        # Check the meeting is not already added
        if len(self.meeting_cache) > 0:
            if m.date == self.meeting_cache[0].date:
                print(f'Duplicate meeting: {m}')
                return

        # Add the meeting
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

    # Run bot
    client.run(token)

