from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed
from datetime import datetime
import nextcord

import requests

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS


class WhiteListModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="WhiteList application",
            custom_id="persistent_modal:whitelist",
            timeout=None,
            #auto_defer=False
        )
        self.mc_online_name = False
        
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
            
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.mc_name.value}")

            if response.status_code == 200:
                print('Utente trovato')
                self.mc_online_name = True
                uid = response.json()['id']
            else:
                print('Utente non trovato')
                print(response)

            uid = response.json()['id']
            avatar_url = f"https://crafatar.com/avatars/{uid}?overlay"
            
            
            minecraft_p = Embed(title="Minecraft", color=nextcord.Color.green())
            minecraft_p.add_field(name="Name:", value=f"`{self.mc_name.value}`", inline=False)
            minecraft_p.add_field(name="UUID:", value=f"`{uid}`", inline=False)
            minecraft_p.add_field(name="Online", value=f"`{self.mc_online_name}`", inline=False)
            if self.mc_online_name:
                minecraft_p.set_thumbnail(url=f"https://crafatar.com/avatars/{uid}?overlay")
            
            discord_p = Embed(title="Discord", color=nextcord.Color.blurple())
            discord_p.add_field(name="Name:", value=f"`{interaction.user.display_name}`", inline=False)
            discord_p.add_field(name="id:", value=f"`{interaction.user.id}`", inline=False)
            discord_p.set_thumbnail(interaction.user.avatar)
            

            reason_p = Embed(title="Application", color=0xffffff)
            if self.reason.value:
                reason_p.add_field(name=" ", value=self.reason.value, inline=False)
            else:
                reason_p.add_field(name=" ", value="`Non pervenuta`", inline=False)
            reason_p.set_footer(text=f'{datetime.now()}')


            await tr.send('<@420976633776832523>', embeds=[minecraft_p, discord_p, reason_p])
            
            in_white = InWhiteListView(interaction.user)
            await tr.send(view=in_white)

            await interaction.response.send_message(f'Application sent !', ephemeral=True)




class WhiteListView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @nextcord.ui.button(
        label='Apply for whitelist', style=nextcord.ButtonStyle.grey, custom_id='whitelist-view:apply'
    )
    async def appy(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(WhiteListModal())


class InWhiteListView(nextcord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)

        self.user = user

    @nextcord.ui.button(
        label='Approve', style=nextcord.ButtonStyle.success, custom_id='whitelist-view:approve'
    )
    async def approve(self, button: nextcord.ui.Button, interaction: Interaction):

        if not self.user:
            await interaction.response.send_message('Error user not found T.T')
            return
        dm = await self.user.create_dm()
        await dm.send(embed=Embed(title="Success !",description="Sei stato aggiunto alla whitelist !", color=nextcord.Colour.green()))
        await interaction.channel.delete()

    @nextcord.ui.button(
        label='Close', style=nextcord.ButtonStyle.danger, custom_id='whitelist-view:close'
    )
    async def close(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.channel.delete()



class Ticket(commands.Cog, name="📄 WhiteList"):
    """WhiteList related commands"""

    COG_EMOJI = "📄"

    def __init__(self, bot: commands.Bot):
        self._bot = bot
            

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        self._bot.add_view(InWhiteListView(None))
        self._bot.add_view(WhiteListView())
        self._bot.add_modal(WhiteListModal())
        



    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='whitelist', description='Manage whitelist system')
    @application_checks.has_permissions(administrator=True)
    async def whitelist(self, interaction: Interaction):
        """Manage whitelist system"""    
        pass

    @whitelist.subcommand(description='add whitelist system to channel')
    @application_checks.has_permissions(administrator=True)
    async def add(self, interaction: Interaction, channel: nextcord.TextChannel):
        "Add whitelist system to specific channel"
        view = WhiteListView()
        info = Embed(title="WhiteLIst - INFO", color=0xffffff)
        info.add_field(name=" ", value="Per accedere alla **whitelist** clicca il tasto qui e completa i campi richiesti, dopo un breve lasso di tempo riceverai una notifica.")
        info.add_field(name=" ", value="Per qualsiasi problema non esitare a chiedere aiuto", inline=False)
        info.add_field(name=" ", value=" <#870609512405540925> <@420976633776832523>", inline=False)
        await channel.send(embed=info, view=view)
        await interaction.response.send_message('View created !', ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))