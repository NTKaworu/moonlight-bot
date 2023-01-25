from nextcord.ext import commands, application_checks
from nextcord import Interaction, Embed, SlashOption
import nextcord, os, psutil, socket, requests

TESTING_GUILD_ID = 870598934421200976 # REMOVE THIS


class Server(commands.Cog, name="💾 Server"):
    """Server commands"""

    COG_EMOJI = "💾"

    def __init__(self, bot: commands.Bot):
        self._bot = bot
        self.script_list = []
        for file in os.listdir('scripts'):
            if file.endswith('.py'):
                self.script_list.append(file)

    @application_checks.is_owner()
    @nextcord.slash_command(guild_ids=[TESTING_GUILD_ID], name='server', description='Server related commands')
    async def server(self, interaction: Interaction):
        pass
    
    @application_checks.is_owner()
    @server.subcommand(description='Display server informations')
    async def info(self, interaction: Interaction):
        cpu = psutil.cpu_percent(1)
        ram = psutil.virtual_memory().percent
        
        if cpu and ram < 35:
            colour = nextcord.Color.green() # Green
        elif cpu and ram < 60: 
            colour = nextcord.Color.yellow() # Yellow
        elif cpu and ram < 80:
            colour = nextcord.Color.orange() # Orange
        else:
            colour = nextcord.Color.red() # Red


        embed = Embed(title='System information', description='server stats', colour=colour)

        embed.add_field(name='Node name', value=os.uname().nodename)
        embed.add_field(name='Machine', value=os.uname().machine, inline=False)

        embed.add_field(name='CPU', value=f'`{cpu}%`', inline=True)
        embed.add_field(name='RAM', value=f'`{ram}%`')

        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except:
            ip = 'error'
        embed.add_field(name='IP', value=f'`{ip}`', inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @application_checks.is_owner()
    @server.subcommand()
    async def script(self, interaction: Interaction):
        pass

    @application_checks.is_owner()
    @script.subcommand(description='Execute server script')
    async def execute(self, interaction: Interaction, script: str = SlashOption(name='script', description='Script name')):
        try:
            os.system(f'python3 scripts/{script}')
            await interaction.response.send_message(embed=Embed(title='Script executed!', colour=nextcord.Colour.green()), ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(embed=Embed(title=e, colour=nextcord.Colour.red()), ephemeral=True)

    @execute.on_autocomplete('script')
    async def script_autocomplete(self, interaction: Interaction, script: str):

        self.script_list = []
        for file in os.listdir('scripts'):
            if file.endswith('.py'):
                self.script_list.append(file)

        if not script:
            await interaction.response.send_autocomplete(self.script_list)
            return
        near_script = [script for script in self.script_list if script.lower().startwith(script.lower())]
        await interaction.response.send_autocomplete(near_script)
    

    @application_checks.is_owner()
    @script.subcommand(description='Remove server script')
    async def remove(self, interaction: Interaction, script: str = SlashOption(name='script', description='Script name')):
        try:
            os.remove(f'scripts/{script}')
            await interaction.response.send_message(f'{script} removed !', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)
    @remove.on_autocomplete('script')
    async def script_autocomplete(self, interaction: Interaction, script: str):

        self.script_list = []
        for file in os.listdir('scripts'):
            if file.endswith('.py'):
                self.script_list.append(file)

        if not script:
            await interaction.response.send_autocomplete(self.script_list)
            return
        near_script = [script for script in self.script_list if script.lower().startwith(script.lower())]
        await interaction.response.send_autocomplete(near_script)


    @script.subcommand(description='Cat a server script')
    async def cat(self, interaction: Interaction, script: str = SlashOption(name='script', description='Script name')):
        try:
            file = nextcord.File(f'scripts/{script}', filename=script)
            await interaction.response.send_message(file=file, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)
    @cat.on_autocomplete('script')
    async def script_autocomplete(self, interaction: Interaction, script: str):

        self.script_list = []
        for file in os.listdir('scripts'):
            if file.endswith('.py'):
                self.script_list.append(file)

        if not script:
            await interaction.response.send_autocomplete(self.script_list)
            return
        near_script = [script for script in self.script_list if script.lower().startwith(script.lower())]
        await interaction.response.send_autocomplete(near_script)

    @server.error
    async def server_error(self, interaction: Interaction, error: commands.CommandError):
        await interaction.response.send_message(error)
    
    @commands.is_owner()
    @commands.command()
    async def push(self, ctx: commands.Context):
        att = ctx.message.attachments
        if att:
            for e in att:
                url = e.url.replace('%27%3E', '')
                response = requests.get(url)
                open(f'scripts/{e.filename}', 'wb').write(response.content)
                embed = Embed(title=f'File {e.filename} loaded !', description=url, colour=nextcord.Colour.green())
                await ctx.send(embed=embed)
        else:
            await ctx.send('error')

        
    
    

def setup(bot: commands.Bot):
    bot.add_cog(Server(bot))