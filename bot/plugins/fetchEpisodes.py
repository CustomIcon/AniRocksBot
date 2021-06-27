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
    if len(data.results) == 0:
        return await query.message.edit(
            '**Episode you requested is not Available at the moment**',
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Back to Episodes', callback_data=f'ep_{anime_id}_{_cache[int(str(query.from_user.id) + str(query.message.message_id))]}')]]
                
            )
        )
    buttons = [
        [
            types.InlineKeyboardButton('Stream', url=data.results[0].link.replace('//', ''))
        ],
        [
            types.InlineKeyboardButton('Download', url=data.results[0].other_server.replace('streaming.php', 'download'))
        ],
        [
            types.InlineKeyboardButton('Back to Episodes', callback_data=f'ep_{anime_id}_{query.data.split("_")[3]}')
        ]
    ]
    await query.message.edit(
        f'**{data.results[0].schedule}**\n**Episode:** __{data.results[0].current_episode_name}__[\u200c\u200c\u200e]({data.results[0].episode_thumbnail})\n',
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )
    await query.answer()
    