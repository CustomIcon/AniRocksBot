from bot import bot
from pyrogram import types, filters


@bot.on_callback_query(filters.regex('^ani_'))
async def anime_handler(_, query: types.CallbackQuery):
    await query.message.edit('**Processing...**')
    anime = await bot.anime_details(query.data.split('_')[1])
    back_s = '\n'
    await query.message.edit(
        f'**{anime.title} ({anime.Othername})** - [{anime.type}]\n**Genres:** {anime.genres}'
        f'\n**Status:** {"".join(anime.status.split())} {anime.relased}{"" if anime.summary == "" else back_s+"**Summary:**"+back_s+anime.summary}'
        f'\n\n__Total {anime.totalepisode} Episodes__[\u200c\u200c\u200e]({anime.image})',
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        'Fetch Episodes',
                        callback_data=f'ep_{query.data.split("_")[1]}_{anime.totalepisode}'
                    )
                ]
            ]
        )
    )