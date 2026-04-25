import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

intents = discord.Intents.default()
intents.message_content = True

CLIENT = Client(intents=intents)
CLIENT.run('YOUR_BOT_TOKEN_HERE')
