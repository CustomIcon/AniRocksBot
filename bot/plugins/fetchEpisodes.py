from bot import bot
from pyrogram import types, filters
from bot.utils.buttons import _cache, page


@bot.on_callback_query(filters.regex(r'ep_'))
async def episode_handler(_, query: types.CallbackQuery):
    await query.message.edit('**Processing...**')
    _cache[int(str(query.from_user.id) + str(query.message.message_id))] = int(query.data.split('_')[2])
    button = page(
                0,
                _cache[int(str(query.from_user.id) + str(query.message.message_id))],
                query.data.split('_')[1],
                'a'
            )
    if button:
        await query.message.edit(
            '**Here are the Available Episodes:**',
            reply_markup=types.InlineKeyboardMarkup(
                button
            )
        )
    else:
        await query.message.edit(
            '**There are no Available Episodes in our Server**'
        )


@bot.on_callback_query(filters.regex(r'a_'), group=4)
async def anime_button(client, query):
    try:
        cache = _cache[int(str(query.from_user.id) + str(query.message.message_id))]
    except KeyError:
        return await query.answer(
            'Error: Message is old.', show_alert=True
        )
    if query.data.startswith('a_p'):
        curr_page = int(query.data.split('_')[3])
        await query.message.edit_reply_markup(
            reply_markup=types.InlineKeyboardMarkup(
                page(curr_page - 1, cache, query.data.split('_')[2], 'a'),
            ),
        )
    elif query.data.startswith('a_n'):
        next_page = int(query.data.split('_')[3])
        await query.message.edit_reply_markup(
            reply_markup=types.InlineKeyboardMarkup(
                page(next_page + 1, cache, query.data.split('_')[2], 'a'),
            ),
        )
    return await client.answer_callback_query(query.id)




@bot.on_callback_query(filters.regex(r'an_'))
async def episode_handler(_, query: types.CallbackQuery):
    await query.message.edit('**Processing...**')
    anime_id = query.data.split('_')[1]
    data = await bot.fetch_episodes(
                anime_id=anime_id, episode=query.data.split('_')[2]
            )
    if len(data.links) == 0:
        return await query.message.edit(
            '**Episode you requested is not Available at the moment**',
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Back to Episodes', callback_data=f'ep_{anime_id}_{_cache[int(str(query.from_user.id) + str(query.message.message_id))]}')]]
                
            )
        )
    buttons = [
        [
            types.InlineKeyboardButton(anime.size, url=anime.src)
            for anime in data.links
        ],
        [
            types.InlineKeyboardButton('Direct Stream', url=f'https://www.aniryu.me/watching/{anime_id}/{query.data.split("_")[2]}')
        ],
        [
            types.InlineKeyboardButton('Back to Episodes', callback_data=f'ep_{anime_id}_{data.totalepisode}')
        ]
    ]
    await query.message.edit(
        'Thank you for using @AniRocksBot. This is an Ad-Free Opensource project, and a One-Man Team Driven Product.\n**Here is your Request:**',
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )
    await query.answer()
    