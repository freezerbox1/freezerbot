import discord
import nest_asyncio
from discord import Message, Intents
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import Final
from responses import *
import random

# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix='$', description="this is a bot", intents=discord.Intents.all())


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message empty because intents not enabled)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


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


@bot.tree.command(name="avatar", description="Get user avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.display_avatar)


nest_asyncio.apply()


# main entry point
def main():
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
