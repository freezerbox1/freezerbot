import discord
import nest_asyncio
from discord import Message, Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
import random
import time

startTime = time.time()


# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix='$', description="this is a bot", intents=discord.Intents.all())


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('ERROR: (Message empty because intents not enabled)')
        return


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is running')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.competing, name="worst bot competition"))
    await bot.tree.sync()


# handling incoming messages

@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}')
    await send_message(message, user_message)


@bot.tree.command(name="kostky", description="Hodí jednoduchou kostku (6 stran).")
async def slash_command(interaction: discord.Interaction):
    await interaction.response.send_message("🎲  " + str(random.randint(1, 6)))


@bot.tree.command(name="avatar", description="returns inputter user avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.display_avatar)


@bot.tree.command(name="uptime", description="returns how long the bot has been online.")
async def uptime(interaction: discord.Interaction):
    rounded_time = round(time.time() - startTime)
    await interaction.response.send_message("Freezerbot has been up for `" + str(round(rounded_time / 60 / 60 / 24)) + " days` / `"  + str(round(rounded_time / 60 / 60)) + " hours.`")


nest_asyncio.apply()


# main entry point
def main():
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
