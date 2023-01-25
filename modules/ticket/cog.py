from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed
import nextcord

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS

class InsideTicketView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label='Close', style=nextcord.ButtonStyle.danger, custom_id='inside-ticket-view:close'
    )
    async def close(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.channel.delete()

class TicketView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label='Minecraft help', style=nextcord.ButtonStyle.success, custom_id='ticket-view:minecraft'
    )
    async def minecraft(self, button: nextcord.ui.Button, interaction: Interaction):
    
        for e in interaction.channel.threads:
            if e.name == f'help - {interaction.user}' or e.name == f'MC help - {interaction.user}':
                await interaction.response.send_message(
                    f'Eror, ticket already created -> {interaction.channel.get_thread(e.id).mention}',
                    ephemeral=True
                    )
                break
        else:
            tr = await interaction.channel.create_thread(name=f'MC help - {interaction.user}')
            view = InsideTicketView()
            await tr.send(interaction.user.mention, view=view)
            await interaction.response.send_message(f'help created {tr.mention}', ephemeral=True)

    @nextcord.ui.button(
        label='General help', style=nextcord.ButtonStyle.blurple, custom_id='ticket-view:general'
    )
    async def general(self, button: nextcord.ui.Button, interaction: Interaction):
        for e in interaction.channel.threads:
            if e.name == f'help - {interaction.user}' or e.name == f'MC help - {interaction.user}':
                await interaction.channel.send('test')
                await interaction.response.send_message(
                    f'Eror, ticket already created -> {interaction.channel.get_thread(e.id).mention}',
                    ephemeral=True
                    )
                break
        else:
            tr = await interaction.channel.create_thread(name=f'help - {interaction.user}')
            view = InsideTicketView()
            await tr.send(interaction.user.mention, view=view)
            await interaction.response.send_message(f'help created {tr.mention}', ephemeral=True)


class Ticket(commands.Cog, name="🎟 Ticket"):
    """Ticket related commands"""

    COG_EMOJI = "🎟"

    def __init__(self, bot: commands.Bot):
        self._bot = bot

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        ticket_view = TicketView()
        inside_ticket_view = InsideTicketView()
        self._bot.add_view(ticket_view)
        self._bot.add_view(inside_ticket_view)



    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='ticket', description='Manage ticket system')
    @application_checks.has_permissions(administrator=True)
    async def ticket(self, interaction: Interaction):
        """Manage ticket system"""    
        pass

    @ticket.subcommand(description='add tiket system to channel')
    @application_checks.has_permissions(administrator=True)
    async def add(self, interaction: Interaction, channel: nextcord.TextChannel):
        "Add ticket system to specific channel"
        view = TicketView()
        await channel.send(view=view)
        await interaction.response.send_message('View created !', ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))