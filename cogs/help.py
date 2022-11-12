import discord
from discord import app_commands
from discord.ext import commands
import os
from datetime import datetime

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.tree.on_error = self.cog_app_command_error
    
    async def cog_load(self) -> None:
        print(' *Help module READY')

    
    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        return await super().cog_app_command_error(interaction, error)


    @app_commands.command(name='help', description='Shows you a list of commands...Or in this case the only command this bot has.')
    async def help(self, interaction: discord.Interaction) -> None:
        '''Help command'''
        # Fetch commands
        commands = await self.bot.tree.fetch_commands()
        embed = discord.Embed(
            title='Help',
            color=discord.Color(0x1DA1F2),
            timestamp=datetime.now(),
        ).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar)
        embed.add_field(
            name=f'{commands[0].mention}',
            value='Adds a checkmark to your current display name.',
            inline=False,
        )
        embed.add_field(
            name='Note',
            value='''
                I cannot change the names of server owners or anyone with a role higher than one I have. 
                As a workaround, make a hidden role and set it higher than roles you want to be able
                to use the command and give it **[manage_nicknames]** permission(s).
                ''',
            inline=False,
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))