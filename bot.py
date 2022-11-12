import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import logging

load_dotenv()

DEFAULT_PREFIX = 'v!'

# Enable Discord Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class VerifyBot(commands.Bot):
    def __init__(self, session):
        super().__init__(
            command_prefix=DEFAULT_PREFIX,
            intents=intents,
            application_id=int(os.getenv('APPLICATION_ID')),
            owner_id=int(os.getenv('OWNER_ID')),
            activity=discord.Game('I believe in free verifications.'),
            status=discord.Status.online,
            help_command=None,
        )
        self.session = session
        self.config_token = str(os.getenv('BOT_TOKEN'))
        self.version = '1.0.0'
        self.DEFAULTPREFIX = DEFAULT_PREFIX
        self.owner_guild_id = os.getenv('OWNER_GUILD_ID')

        logging.basicConfig(level=logging.INFO)

        self.initial_extensions = [
            'cogs.verify',
            'cogs.help'
        ]


    async def setup_hook(self) -> None:
        print('Running setup...')
        self.session = aiohttp.ClientSession()

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        # self.tree.copy_global_to(guild=discord.Object(id=self.owner_guild_id))
        # await self.tree.sync(guild=discord.Object(id=self.owner_guild_id))
        await self.tree.sync()
        print('Slash commands synced...')
        print('Setup complete...')

    
    async def close(self) -> None:
        await super().close()
        await self.session.close()

    
    async def on_ready(self) -> None:
        await self.wait_until_ready()
        print('Ready.')


    async def on_message(self, message):
        if message.author.id == self.user.id: # ignore self
            return
        await self.process_commands(message)


async def main():
    async with aiohttp.ClientSession() as session:
        async with VerifyBot(session) as bot:
            await bot.start(bot.config_token)


asyncio.run(main())