#!/usr/bin/python3

import ast
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        meeting_dates_cache = set({})
        target_channel = ''

        # Get meeting dates cache from file
        try:
            with open('cfbt-cache.txt', 'r') as f:
                self.meeting_dates_cache = ast.literal_eval(f.read())
        except FileNotFoundError:
            pass

        # Get meeting agenda output channel ID
        with open('channel.txt', 'r') as f:
            self.target_channel = f.readline().strip()
        print(f'Sending meeting agendas to channel ID {self.target_channel}')

    async def on_ready(self):
        """Runs when the bot connects successfully"""

        print(f'Logged on as {self.user}')

        print(f'Starting update task loop')
        self.update.start()

    @tasks.loop(seconds=5.0)
    async def update(self):
        """Event loop for checking for new meetings"""
        self.add_meeting(cor.get_recent())

    def add_meeting(self, m):
        """Add a meeting to the meeting cache"""

        # Check the meeting is not already added
        if m.date not in self.meeting_dates_cache:

            # Add the meeting
            self.meeting_dates_cache.add(m.date)
            print(f'New meeting: {m}')

            # Update the cache
            with open('cfbt-cache.txt', 'w') as f:
                f.write(str(self.meeting_dates_cache))
            print('Updated cache')

        else:
            print(f'Duplicate meeting: {m}')

if __name__ == '__main__':

    # Get secret token from file
    token = ''
    with open('token.txt', 'r') as f:
        token = f.readline()

    # Create and run bot
    intents = discord.Intents.default()
    # Following line is necessary for newer versions of discord.py,
    #    but does not work for the version compatible with cs1 
    # intents.message_content = True
    client = BetterTransitBot(command_prefix='!', intents=intents)

    # Run bot
    client.run(token)

