#!/usr/bin/env python3

import json

from telethon import events, hints


async def send_help(
        channel: hints.EntityLike,
        event) -> None:
    """send /pthelp command help."""
    help_top = """**PT入门资料(内含常见问题解决方法):**
[PT指南和教程](https://github.com/Suwmlee/Christina/files/5840869/PT.pdf)  [从零开始玩PT_V1.0_2](https://github.com/Suwmlee/Christina/files/5840885/PT_V1.0_2.pdf) \n"""
    help_foot = """**常见问题**
Could not connect to tracker/无法连接tracker服务器/黄种
    `与tracker服务器连接不稳定,没有汇报成功.解决方法:1)等待下次汇报恢复;2)强制重新汇报;3)改善网络环境`
提问题前麻烦先查询历史记录与置顶"""
    help_site = ""
    if channel.id == 1051902747:
        # m-team
        help_site = """\n[**M-Team Wiki <-点这里**](https://wiki.m-team.cc/index.php?title=%E9%A6%96%E9%A0%81) 
[**M-Team 封禁查询**](https://pt.m-team.cc/userban.php?action=list)
[**M-Team 24小时自助注册**](https://pt.m-team.cc/pay.php)
[**M-Team 多电脑上传/下载**](https://wiki.m-team.cc/index.php?title=%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E5%A4%9A%E5%8F%B0%E9%9B%BB%E8%85%A6%E7%99%BB%E5%85%A5%E6%88%96%E9%80%B2%E8%A1%8C%E4%B8%8A%E5%82%B3/%E4%B8%8B%E8%BC%89%E5%97%8E%EF%BC%9F)
[**M-Team 保号说明**]https://wiki.m-team.cc/index.php?title=%E5%B8%B3%E8%99%9F%E4%BF%9D%E7%95%99%E8%A6%8F%E5%89%87) \n"""
    elif channel.id == 1542127638:
        # t-bot 
        help_site = ""
    full = help_top + help_site + help_foot
    help_message = await event.reply(
        full,
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
        await send_help(to_chat, event)
