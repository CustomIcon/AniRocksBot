from pyrogram import types
from math import ceil

_cache = {}


class EqInlineKeyboardButton(types.InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text
    def __lt__(self, other):
        return self.text < other.text
    def __gt__(self, other):
        return self.text > other.text


def range1(start, end):
    return range(start, end+1)


def page(page_n, episodes, anime_id, prefix):
    ep = [EqInlineKeyboardButton(
            f"Ep.{episode}",
            callback_data='an_{}_{}'.format(anime_id, episode)
        ) for episode in range1(1, int(episodes))]
    pairs = list(zip(ep[::3], ep[1::3], ep[2::3]))
    c = 0
    for x in pairs:
        for _ in x:
            c += 1
    if len(ep) - c == 1:
        pairs.append((ep[-1],))
    elif len(ep) - c == 2:
        pairs.append(
            (
                ep[-2],
                ep[-1],
            ),
        )
    if int(episodes) == 0:
        return None
    max_num_pages = ceil(len(pairs) / 3)
    modulo_page = page_n % max_num_pages
    if len(pairs) > 3:
        pairs = pairs[modulo_page * 3: 3 * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    'previous', callback_data=f'{prefix}_p_{anime_id}_{modulo_page}',
                ),
                EqInlineKeyboardButton(
                    'next', callback_data=f'{prefix}_n_{anime_id}_{modulo_page}',
                ),
            ),
        ]
    return pairs