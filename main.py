import os, nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

# -------------------------> Intents <-------------------------- #
intents = nextcord.Intents.default()
intents.message_content = True
# ------------------------------------------------------------ #

# -------------------------> Activity <-------------------------- #
activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="chiunque abbia bisognoi")
# ------------------------------------------------------------ #

# ------------------------> Main loop <------------------------- #
def main():
    bot = commands.Bot(
        command_prefix='-',
        activity=activity,
        intents=intents
        )
    bot.remove_command('help')

    load_dotenv()

    # On ready event
    @bot.event
    async def on_ready():
        print(f"{bot.user.name} is ready and connected to Discord.")

    # Load all cogs
    for folder in os.listdir("modules"):
        if os.path.exists(os.path.join("modules", folder, "cog.py")):
            bot.load_extension(f"modules.{folder}.cog")

    bot.run(os.getenv("DISCORD_TOKEN"))
# ------------------------------------------------------------ #


if __name__ == '__main__':
    main()
