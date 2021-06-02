from bot import bot
from pyrogram import filters, types
import os
from bot.utils.run_cmd import screen_shot, take_screen_shot
import tracemoepy
import aiohttp
import asyncio


@bot.on_message(
    filters.photo | filters.video | filters.animation
)
async def tracemoe_rs(client, message):
    _loc = ''
    dis = await client.download_media(
        message=message,
        file_name=screen_shot,
    )
    _loc = os.path.join(screen_shot, os.path.basename(dis))
    if message.animation:
        img_file = os.path.join(screen_shot, 'grs.jpg')
        await take_screen_shot(_loc, 0, img_file)
        _loc = img_file
    if message.video:
        nama = 'video_{}-{}.mp4'.format(
            message.reply_to_message.video.date,
            message.reply_to_message.video.file_size,
        )
        await client.download_media(
            message.reply_to_message.video,
            file_name='downloads/' + nama,
        )
        _loc = 'downloads/' + nama
        img_file = os.path.join(screen_shot, 'grs.jpg')
        await take_screen_shot(_loc, 0, img_file)
    session = aiohttp.ClientSession()
    tracemoe = tracemoepy.AsyncTrace(session=session)
    if message.photo:
        img_file = await message.download()
        search = await tracemoe.search(img_file, upload_file=True)
        os.remove(img_file)
    else:
        search = await tracemoe.search(_loc, upload_file=True)
    os.remove(_loc)
    result = search['docs'][0]
    if not result['title_english']:
        return await message.reply('**Cannot find any results**')
    text = (
        f"**{result['title_english']}**"
        f"\n{round(result['similarity']*100, 2)}% Similarity"
        f"\n__Episode {result['episode']}__"
    )
    await asyncio.gather(
        message.reply(
            text,
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [
                        types.InlineKeyboardButton(
                            'Get Anime',
                            callback_data=f's_{result["title_english"]}'
                        )
                    ]
                ]
            )
        ),
        tracemoe.aio_session.close()
    )
