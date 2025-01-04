#!/usr/bin/python3

import asyncio
import discord
from discord.ext import commands

import cor

# TODO: - use tasks 
# https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
# - make cor meetings cog
# - make events cog
# https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html

class BetterTransitBot(commands.Bot):

    meeting_cache = []
    target_channel = ''

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        # Initialize meetings
        await self.update()

    async def update(self):
        print('Starting update loop')
        while True:
            client.add_meeting(cor.get_meeting())
            await asyncio.sleep(1)

    @commands.command()
    async def target(self, ctx):
        await ctx.send(f'Target channel {ctx.channel}')

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

