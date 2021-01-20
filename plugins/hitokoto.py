#!/usr/bin/env python3

import json
import requests

from telethon import events, hints


hiturl = "https://v1.hitokoto.cn/?encode=json"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


async def get_hitokoto():
    """ get hitokoto.
    """
    ret = None
    try:
        res = requests.get(hiturl, headers=headers)
        if res.status_code == 200:
            result = json.loads(res.text)
            ret = 'Hitokoto No:' + str(result['id']) + '\n' + result['hitokoto'] + '\n' + '—— by ' + result['creator']
            if 'from' in result and result['from'] != '' and result['from'] != result['creator']:
                ret = ret + ' (' + result['from'] + ')'
            # else:
            #     print(result['from'])
            # print(ret)
    except:
        pass
    return ret


async def send_hitokoto(
        channel: hints.EntityLike,
        event) -> None:
    """send hitokoto."""
    retmsg = await get_hitokoto()
    if not retmsg:
        return
    hitokoto_message = await userbot.send_message(channel, retmsg)


@userbot.on(events.NewMessage(pattern="/oneword"))
async def generate_hitokoto_from_event(event) -> None:
    """generate word cloud based on event."""
    msg = event.message
    if (not msg.text) or (not msg.text.lower().startswith("/oneword")):
        return
    to_chat = await event.get_chat()

    _, *rest = msg.text.lower().split(" ")

    if not rest:
        await send_hitokoto(to_chat, event)


if __name__ == "__main__":
    get_hitokoto()
