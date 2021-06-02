from bot import bot
from pyrogram import filters, types

__header__='📕 **Page** {} of 4\n\n'

@bot.on_message(
    filters.command("start"), group=-1
)
async def alive(_, message):
    await message.reply(
        f'Hello {message.from_user.mention},\n'
        'Please read the documentation below on how to use @AniRocksBot before doing anything else:',
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton('read the brief documentation here',callback_data='docs_1')]]
        )
    )

@bot.on_callback_query(filters.regex('^docs_'))
async def docs_btn(_, query):
    data = query.data.split('_')[1]
    if data == '1':
        return await query.message.edit(
            __header__.format(data)
            + 'The bot has no command involved in it to search anime. so you have to directly type in an anime you want to get the stream link of',
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Page 2', callback_data='docs_2')]]
            )
        )
    elif data == '2':
        return await query.message.edit(
            __header__.format(data)
            + 'For Example you can type in `naruto` and the bot will give you the result. Rest is up for you to press on which anime you like to choose',
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Page 3', callback_data='docs_3')]]
            )
        )
    elif data == '3':
        return await query.message.edit(
            __header__.format(data)
            + 'You can also Reverse Search an anime clip simply by sending a video, gif or a photo and get the details to download the Anime',
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton('Page 4', callback_data='docs_4')]]
            )
        )
    elif data == '4':
        return await query.message.edit(
            __header__.format(data)
            + 'That is the end of the documentation. if you face an Issue on the bot, please report to the support chat. Developer will fix the issue soon as possible. @AniRocksBot is a one man team product made on purpuse to serve Telegram users Anime without a delay.',
            reply_markup=types.InlineKeyboardMarkup(
                [
                    [types.InlineKeyboardButton("Let's get started", callback_data='docs_end')],
                    [
                        types.InlineKeyboardButton('Repository', url='https://github.com/pokurt/AniRocksBot'),
                        types.InlineKeyboardButton('Support', url='https://t.me/joinchat/3AONXaLAJa4yYzhl')
                    ]
                ]
            )
        )
    elif data == 'end':
        return await query.message.edit(
            '**Well Done!**\nType in any Anime you want to get the stream link:'
        )