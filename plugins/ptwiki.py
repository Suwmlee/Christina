#!/usr/bin/env python3

import json

from telethon import events, hints


async def send_help(event) -> None:
    """send /pthelp command help."""
    help_message = await event.reply(
        " [PT入门指南](https://cowtransfer.com/s/d25f43470d6f40) \n"
        " [M-Team Wiki](https://wiki.m-team.cc/index.php?title=%E9%A6%96%E9%A0%81)"
    )


@userbot.on(events.NewMessage(pattern="/pthelp"))
async def generate_ptwiki_from_event(event) -> None:
    """generate pthelp based on event."""
    msg = event.message
    if (not msg.text) or (not msg.text.lower().startswith("/pthelp")):
        return
    to_chat = await event.get_chat()

    _, *rest = msg.text.lower().split(" ")

    if not rest:
        await send_help(event)