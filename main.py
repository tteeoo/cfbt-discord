import discord

class BetterTransitBot(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

token = ''
with open('token.txt', 'r') as f:
    token = f.readline()

client = BetterTransitBot(intents=intents)
client.run(token)
