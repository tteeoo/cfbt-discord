#!/usr/bin/python3

import ast
import asyncio
import os

import discord
from discord.ext import commands, tasks

import cor

# TODO:
# - safety on cache file?
# - make cor meetings cog (cogs: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
# - make events cog to update website?

# Configuration variables
PREFIX_DIR = 'share'
TOKEN_FILE = os.path.join(PREFIX_DIR, 'token.txt')
CHANNEL_FILE = os.path.join(PREFIX_DIR, 'channel.txt')
CACHE_FILE = os.path.join(PREFIX_DIR, 'cache.txt')

class BetterTransitBot(commands.Bot):
    """Holds a target channel and a cache of noticed meetings.
       Periodically checks for new meetings if found, sends a message."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.meeting_dates_cache = set({})
        self.target_channel = None

        # Get meeting dates cache from file
        try:
            with open(CACHE_FILE, 'r') as f:
                self.meeting_dates_cache = ast.literal_eval(f.read())
        except FileNotFoundError:
            pass


    async def on_ready(self):
        """Runs when the bot connects successfully"""

        print(f'Logged on as {self.user}')

        # Get meeting agenda output channel ID
        cid = -1
        with open(CHANNEL_FILE, 'r') as f:
            cid = int(f.readline().strip())
            self.target_channel = self.get_channel(cid)
        print(f'Target channel set to {self.target_channel} (ID: {cid})')

        print(f'Starting update task loop')
        self.update.start()

    @tasks.loop(seconds=5.0)
    async def update(self):
        """Event loop for checking for new meetings"""
        await self.add_meeting(cor.get_recent())

    async def add_meeting(self, m):
        """Add a meeting to the meeting cache"""

        # Check the meeting is not already added
        if m.date not in self.meeting_dates_cache:

            # Add the meeting
            self.meeting_dates_cache.add(m.date)
            print(f'New meeting: {m}')
            # Send the message
            print('Sending message to channel')
            await self.send_meeting_message(m)

            # Update the cache
            with open(CACHE_FILE, 'w') as f:
                f.write(str(self.meeting_dates_cache))
            print('Updated cache')

        else:
            print(f'Duplicate meeting: {m}')

    async def send_meeting_message(self, m):
        """Send a message to the target channel about the given new meeting"""

        content = f"A New City of Richardson City Council meeting agenda for {m.date} has been posted. Here's the link: {m.agenda}"

        await self.target_channel.send(content=content)
        

if __name__ == '__main__':

    # Get secret token from file
    token = ''
    with open(TOKEN_FILE, 'r') as f:
        token = f.readline()

    # Create and run bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = BetterTransitBot(command_prefix='!', intents=intents)

    # Run bot
    client.run(token)
