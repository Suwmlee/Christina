#!/usr/bin/env python3

import json

from telethon import events, hints


async def send_help(event) -> None:
    """send /pthelp command help."""
    help_message = await event.reply(
        "[PT指南(解决80%问题)](https://cowtransfer.com/s/d25f43470d6f40) \n"
        "[M-Team Wiki](https://wiki.m-team.cc/index.php?title=%E9%A6%96%E9%A0%81) \n"
        "[M-Team 封禁查询](https://pt.m-team.cc/userban.php?action=list) \n"
        "**常见问题** \n"
        "Could not connect to tracker/无法连接tracker服务器/黄种 \n"
        "`与tracker服务器连接不稳定,汇报没有成功.解决方法:1)等待下次更新恢复;2)强制重新汇报;3)改善网络环境`",
        link_preview=False
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
