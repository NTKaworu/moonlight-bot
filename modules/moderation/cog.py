from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed, SlashOption
import nextcord, humanfriendly, datetime

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS


class Moderation(commands.Cog, name="🚨 Moderation"):
    """Moderation commands"""

    COG_EMOJI = "🚨"

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self.mute_options = [
            '60 sec',
            '5 min',
            '10 min',
            '1 hour',
            '1 day',
            '1 week',
        ]

    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='purge', description='Clear messages')
    async def purge(self, interaction: Interaction, amount: int):

        if amount > 100:
            await interaction.response.send_message(f'Soglia di messaggi superati {amount}/100', ephemeral=True)
            amount = 100

        delated = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f'{len(delated)} messaggi sono stati cancellati', ephemeral=True)

    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='mute', description='Mute a specific user')
    async def mute(self, interaction: Interaction, user: nextcord.User, time: str = SlashOption(name='mute', description='mute time'), reason: str = None):

        time = humanfriendly.parse_timespan(time)

        guild = interaction.guild
        member = guild.get_member(user.id)

        await member.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=time))
        await interaction.response.send_message(f"{member} è stato mutato per {reason}")
    
    @application_checks.is_owner()
    @mute.on_autocomplete('time')
    async def time_options(self, interaction: Interaction, time: str):
        if not time:
            await interaction.response.send_autocomplete(self.mute_options)
            return
        get_near_option = [option for option in self.mute_options if option.lower().startswith(time.lower())]
        await interaction.response.send_autocomplete(get_near_option)
        
    
    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='say', description='Make the bot say something')
    async def say(self, interaction: Interaction, text: str):
        await interaction.channel.send(text)
        await interaction.response.send_message('Message sent !', ephemeral=True)
    
    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='embed', description='Make the bot sand an embed')
    async def embed(self, interaction: Interaction, title: str, description: str):
        await interaction.channel.send(embed=Embed(title=title, description=description))
        await interaction.response.send_message('Embed sent !', ephemeral=True)
    

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))