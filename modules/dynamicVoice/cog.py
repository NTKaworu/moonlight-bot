from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed
import nextcord

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS
VOICE_CATEGORY = '870609690176946246'
VOICE_TEXT = '870610393586864138'

class DynamicVoice(commands.Cog, name="🔊 Voice"):
    """Voice commands"""

    COG_EMOJI = "🔊"

    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if before.channel is None and after.channel is not None:
            # entra nel canale vocale

            if str(after.channel.category_id) == VOICE_CATEGORY:
                if not len(after.channel.members) > 1:
                    await after.channel.clone(name='🔊 Voice', reason='dynamic voice channels')

        elif before.channel is not None and after.channel is None:
            # esce dal canale vocale
            
            if str(before.channel.category_id) == VOICE_CATEGORY:
                if len(before.channel.members) < 1 and len(before.channel.category.voice_channels) > 1:
                    await before.channel.delete()
            
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:

            if str(before.channel.category_id) == VOICE_CATEGORY:
                if len(before.channel.members) < 1 and len(before.channel.category.voice_channels) > 2:
                    await before.channel.delete()
                        
            


    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='voice', description='Create a voice channel')
    async def voice(self, interaction: Interaction, name: str):
        """Creates a voice channel"""    

        if str(interaction.channel.category.id) == VOICE_CATEGORY:
            new_voice = await interaction.channel.category.create_voice_channel(name=name)
            await interaction.response.send_message(f'Channel created {new_voice.mention}', ephemeral=True)
        else:
            await interaction.response.send_message(f'You have to be in this <#{VOICE_TEXT}> category to perform the command', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(DynamicVoice(bot))