from bot import bot
from pyrogram import types, filters


@bot.on_callback_query(filters.regex('^ani_'))
async def anime_handler(_, query: types.CallbackQuery):
    await query.message.edit('**Processing...**')
    anime = await bot.anime_details(query.data.split('_')[1])
    try:
        ani = anime.results[0]
    except IndexError:
        return await query.message.edit('Cannot Resolve Anime Details')
    back_s = '\n'
    await query.message.edit(
        f'**{ani.title} ({ani.native})** - [{ani.format}]\n**Genres:** {ani.genres}'
        f'\n**Status:** {"".join(ani.status.split())} {"" if ani.summary == "" else back_s+"**Summary:**"+back_s+ani.summary}'
        f'\n\n__Total {len(anime.result)} Episodes__[\u200c\u200c\u200e]({ani.image})',
        reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton(
                        'Fetch Episodes',
                        callback_data=f'ep_{query.data.split("_")[1]}_{len(anime.result)}'
                    )
                ]
            ]
        )
    )