import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import weapons


load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


@bot.event
async def on_ready():
    await weapons.init()
    print(f"{bot.user} is now running.")

    await bot.tree.sync()
    print("Command tree synced.")


@bot.tree.command(description="Basic slash command to test if the bot is online or not.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)


@bot.tree.command(description="Get information about a weapon in Castle Crashers.")
async def weapon(interaction: discord.Interaction, name: str = None, id: int = None):
    return await weapons.handle_weapon(interaction, name, id, True)


if __name__ == '__main__':
    bot.run(TOKEN)
