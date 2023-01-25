from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed
from datetime import datetime
import nextcord

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS


class WhiteListModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="WhiteList application",
            custom_id="persistent_modal:whitelist",
            timeout=None,
        )
        
        self.mc_name = nextcord.ui.TextInput(
            label="Come ti chiami su minecraft ?", # Inserisci il tuo nome di minecraft
            placeholder="inserisci il tuo nikname",
            required=True,
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:mc_name",
        )
        self.add_item(self.mc_name)

        self.reason = nextcord.ui.TextInput(
            label="Per quale motivo vuoi entrare ?", #Per quale motivo vorresti entrare nel server ?
            placeholder="Spiega in poche parole se sei stato invitato da qualcuno o per quale motivo vuoi giocare nel server",
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            custom_id="persistent_modal:reason",
        )
        self.add_item(self.reason)
    
    async def callback(self, interaction: nextcord.Interaction):

        for e in interaction.channel.threads:
            if e.name == f'application - {interaction.user}':
                await interaction.response.send_message(
                    f'Eror, you have already made an application, for more information contact Kaworu#0250',
                    ephemeral=True
                    )
                break
        else:
            tr = await interaction.channel.create_thread(name=f'application - {interaction.user}')
            
            

            message = Embed(title=self.mc_name.value, color=nextcord.Color.green())
            message.add_field(name='Reason: ', value=self.reason.value, inline=False)
            message.add_field(name='Discord: ', value=interaction.user.display_name, inline=False)

            message.set_thumbnail(interaction.user.avatar)
            message.set_footer(text=f'{datetime.now()}')

            await tr.send(embed=message)
            await tr.send('<@420976633776832523>')
            await interaction.response.send_message(f'Application sent !', ephemeral=True)




class WhiteListView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label='Apply for whitelist', style=nextcord.ButtonStyle.success, custom_id='whitelist-view:apply'
    )
    async def appy(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(WhiteListModal())



class Ticket(commands.Cog, name="📄 WhiteList"):
    """WhiteList related commands"""

    COG_EMOJI = "📄"

    def __init__(self, bot: commands.Bot):
        self._bot = bot
            

    @commands.Cog.listener('on_ready')
    async def on_ready(self):

        self._bot.add_view(WhiteListView())
        self._bot.add_modal(WhiteListModal())
        



    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='whitelist', description='Manage whitelist system')
    @application_checks.has_permissions(administrator=True)
    async def whitelist(self, interaction: Interaction):
        """Manage whitelist system"""    
        pass

    @whitelist.subcommand(description='add tiket system to channel')
    @application_checks.has_permissions(administrator=True)
    async def add(self, interaction: Interaction, channel: nextcord.TextChannel):
        "Add ticket system to specific channel"
        view = WhiteListView()
        await channel.send(view=view)
        await interaction.response.send_message('View created !', ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))