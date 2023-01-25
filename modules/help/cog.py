from nextcord.ext import commands
from nextcord import Interaction, Embed
import nextcord

from nextcord.ext.commands.help import MinimalHelpCommand

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS

class Help(commands.Cog, MinimalHelpCommand, name="❔ Help"):
    """Receives ping commands"""

    COG_EMOJI = "❔"

    def __init__(self, bot: commands.Bot):
        self._bot = bot


    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='help', description='Gives help')
    async def help(self, interaction: Interaction):
        """Checks for a response from the bot"""   

        help_map = {}
        cogs_map = self._bot.cogs
        for key in cogs_map:
            print(key)
            commands = cogs_map[key].application_commands
            c_list = []
            for e in commands:
                c_list.append((e.name, e.description))

            help_map[key] = c_list
        
        embed = Embed(title='Help', colour=nextcord.Colour.purple())
        for key in help_map:
            #print(key)
            
            li = []
            for e in help_map[key]:
                li.append(f'**{e[0]}**: {e[1]}')
                # aaa: bbb, ccc: ddd
                #print('-')
            tmp = '\n'.join(li)
            embed.add_field(name=key, value=tmp)
        

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))