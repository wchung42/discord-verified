import discord
from discord import app_commands
from discord.ext import commands
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Verify(commands.Cog):
    '''Verify Module'''
    OWNER_GUILD_ID = os.getenv('OWNER_GUILD_ID')

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.tree.on_error = self.cog_app_command_error

    
    async def cog_load(self) -> None:
        print(' *Verification module READY')

    
    async def cog_app_command_error(self, interaction: discord.Interaction, error) -> None:
        # I need to find a way to deal with multiple exception being catched at once
        # Causing an "interaction has already been responded to" exception to be raised
        # Interactions can only be responded to once
        embed = discord.Embed(
            title='ERROR',
            color=discord.Color(0xFF0000),
            timestamp=datetime.now(),
        ).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar)
        print(error)
        if isinstance(error, app_commands.BotMissingPermissions):
            embed.description = f'I am missing {error.missing_permissions} permissions.'
        elif isinstance(error, discord.HTTPException):
            embed.description = f'Your current nickname is too long.'
        elif isinstance(error, app_commands.CommandInvokeError):
            embed.description = 'If you are the server owner or someone more powerful than the bot, unfortunately I cannot change your nickname.'
            embed.add_field(name='Copy and paste', value=f'{interaction.user.display_name} ✔', inline=True)
        elif isinstance(error, discord.Forbidden):
            pass
        else:
            embed.description = 'Unknown error occurred. Please try again.'
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name='verifyme', description='"Verifies" you on the server.')
    @app_commands.checks.bot_has_permissions(manage_nicknames=True)
    async def verify(self, interaction: discord.Interaction) -> None:
        '''Adds a checkmark to the user's current display name.'''
        # Edit current display name with check
        check = '✔'
        await interaction.user.edit(nick=f'{interaction.user.display_name} {check}')

        # Get "verify_counter" collection
        db = self.bot.mongoConnect['counters']
        collection = db['verify_counter']

        # Check if "verifies" counter is already in collection, if not then create and insert
        if await collection.find_one({'_id': 'verifies'}) is None:
            new_data = {
                '_id': 'verifies',
                'count': 1
            }
            await collection.insert_one(new_data)
        else:
            # Increment counter in db
            await collection.update_one(
                {'_id': 'verifies'},
                {'$inc': {'count': 1}}, 
            )

        # Send interaction response
        await interaction.response.send_message(content=':white_check_mark: Verified! :white_check_mark:')


    @app_commands.command(name='count', description='Returns number of successful verifications.')
    async def count(self, interaction: discord.Interaction) -> None:
        '''Shows number of successful verifications.'''
        # Get "verify_counter" collection
        db = self.bot.mongoConnect['counters']
        collection = db['verify_counter']

        # Get verifies count
        try:
            result = await collection.find_one({'_id': 'verifies'})
        except Exception as e:
            await interaction.response.send_message('ERROR: Could not fetch from database.')
        else:
            verify_cnt = result['count']
            await interaction.response.send_message(f'**{verify_cnt}** members verified!')



    # Default ping command for testing purposes; Uncomment to use this test command
    # @app_commands.command(name='ping', description='Pong.')
    # # @app_commands.guilds(discord.Object(id=200372022549676032))
    # async def ping(self, interaction: discord.Interaction) -> None:
    #     '''Ping command'''
    #     await interaction.response.send_message(f'Pong! {round(self.bot.latency*1000)}ms')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Verify(bot))