from bot import bot
from pyrogram import filters


@bot.on_message(
    filters.command("start"), group=-1
)
async def alive(_, message):
    await message.reply('Hi I am Alive')