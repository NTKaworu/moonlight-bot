from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed
import nextcord

TESTING_GUILD_ID = 870598934421200976  # REMOVE THIS

class Info(commands.Cog, name="ℹ️ Info"):
    """Receives info commands"""

    COG_EMOJI = "ℹ️"

    def __init__(self, bot: commands.Bot):
        self._bot = bot


    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='info', description='Print server iformation')
    async def print_info(self, interaction: Interaction):
        """Print minecraft info"""
        white = Embed(title='WHITELIST', color=0xffffff)
        white.add_field(name=" ", value="Per entrare nel server è necessario essere nella whitelist. Per registrarsi seguire i passaggi nel canale apposito")
        white.add_field(name=" ", value="<#1062647569597079572>")


        primo = Embed(title="Minecraft Server - INFO", color=0x00ff2a)
        primo.add_field(name=" ", value="Per accedere al server basta connettersi all'ip  `2.59.156.46 ` Il server è aperto 24/7 - tempo di manutenzione se necessario")

        secondo = Embed(title='BedRock - INFO', color=0x00d5ff)
        secondo.add_field(name=" ", value="Per accedere da BedRock è semplicissimo, basta accedere allo stesso ip di java usando la porta di default di BedRock o meglio la porta  `19132`")

        terzo = Embed(title='Command - INFO', description="Sono disponibili diversi comandi all'interno del server, di seguito elencati quelli più comuni", color=0xff00c8)
        terzo.add_field(name=" ", value='`/home` : Serve per teletrasportarsi alla propria home _(se non è impostata al letto)_')
        terzo.add_field(name=" ", value='`/sethome` : Serve per salvare la posizione della propria home')
        terzo.add_field(name=" ", value='`/removehome home` : Serve eliminare la propria home')
        terzo.add_field(name=" ", value='`/spawn` : Serve per teletrasportarsi allo spawn del server')
        terzo.add_field(name=" ", value='`/msg < player name >` : Serve a inviare messaggi privati ad un player')
        terzo.add_field(name=" ", value='`/dynmap hide` : Serve a nascondere la propria posizione sulla mappa online')
        terzo.add_field(name=" ", value='`/dynmap show` : Serve a nascondere la propria posizione sulla mappa online')

        quarto = Embed(title='Map - INFO', color=0xff0000)
        quarto.add_field(name=" ", value="Per accedere al sito della mappa dinamica del server basta reacarsi all'indirizzo ip del server usando un browser. `http://2.59.156.46/`")
        quarto.add_field(name=" ", value="Per aggiungere **icone** o **confini** sulla mappa è necessario contattare <@420976633776832523>")

        quinto = Embed(title='Discord - INFO',description="Sotto la categoria MINECRAFT sono presenti divesi canali realativi al server", color=0x1e77eb)
        quinto.add_field(name=" ", value="Il canale testuale <#870611929717166080> Permette agli utenti di discord di comunicare con i player online sul server di minecraft tramite una chat sincronizzata")
        quinto.add_field(name=" ", value="Il canale vocale <#870611892446593024> Permette di utilizzare la chat vocale dinamica all'interno del gioco. Per abilitare questa funzione è necessario collegare discord al proprio account di minecraft eseguendo su discord il comando `/link`")

        sesto = Embed(title="Contacts", description="Per qualsiasi informazione, dubbio o richiesta non esitate ad aprire un ticket o a chiedere aiuto in privato", color=0xffc800)
        sesto.add_field(name=" ", value="<@420976633776832523> <#870609512405540925>")


        await interaction.channel.send(embeds=[white, primo, secondo, terzo, quarto, quinto, sesto])
        await interaction.response.send_message("Operation complete", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
