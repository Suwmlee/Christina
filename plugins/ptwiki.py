#!/usr/bin/env python3

import asyncio
import json
import datetime

from telethon import events, hints

records = dict()

async def send_help(
        channel: hints.EntityLike,
        event) -> None:
    """send /pthelp command help."""
    help_top = """**PT入门资料(内含常见问题解答):**
[PT指南和教程](https://suwmlee.github.io/docs/PT_intro.pdf)
[从零开始玩PT_V1.0_2](https://suwmlee.github.io/docs/PT_Guide_V1.0_2.pdf)
[必备浏览器插件  PT助手(PTPP)](https://github.com/ronggang/PT-Plugin-Plus)
[PT一键转种        easy-upload](https://github.com/techmovie/easy-upload)
[种子文件修改器](https://github.com/torrent-file-editor/torrent-file-editor)
`转种时，请不要修改文件名`
**进阶**
[IYUU自动辅种工具       最简配置(含群辉等设置)](https://www.iyuu.cn/archives/324/)
[cross-seed                    基于Jackett辅种工具](https://github.com/mmgoodnow/cross-seed)
[flexget+nexusphp       自动订阅/过滤优惠种子(free)等](https://github.com/Juszoe/flexget-nexusphp)
[autoremove-torrents  自动删种程序](https://autoremove-torrents.readthedocs.io/zh_CN/latest/)
[盒子入门(仅参考)](https://yukino.nl/2019/08/10/pt-tools/)
[Aniverse wiki(含PT限盒等统计)](https://github.com/Aniverse/wiki)
**压制入门/深入**
[压制指南(在线预览)](https://suwmlee.github.io/encoding-guide/)
[旧版 Encoding Guide](https://suwmlee.github.io/docs/AHD_encode_guide.pdf)
"""
    help_foot = ""
#     help_foot = """**常见问题**
# Could not connect to tracker/黄种
#     `与tracker服务器连接不稳定,没有汇报成功.解决方法:1)等待下次汇报恢复;2)强制重新汇报;3)改善网络环境`
# 提问题前麻烦先查询历史记录与置顶
# """
    help_site = ""
    if channel.id == 1051902747:
        # m-team
        help_site = ""
    elif channel.id == 1542127638:
        # t-bot 
        help_site = """**[M-Team Wiki <-点这里](https://wiki.m-team.cc/index.php?title=%E9%A6%96%E9%A0%81)**
**[M-Team 封禁查询](https://kp.m-team.cc/userban.php?action=list)**
**[M-Team 盒子及獨立主機特別說明](https://wiki.m-team.cc/index.php?title=%E7%9B%92%E5%AD%90%E5%8F%8A%E7%8D%A8%E7%AB%8B%E4%B8%BB%E6%A9%9F%E7%89%B9%E5%88%A5%E8%AA%AA%E6%98%8E)**
**[M-Team 可以使用多台電腦登入或進行上傳/下載嗎？](https://wiki.m-team.cc/index.php?title=%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E5%A4%9A%E5%8F%B0%E9%9B%BB%E8%85%A6%E7%99%BB%E5%85%A5%E6%88%96%E9%80%B2%E8%A1%8C%E4%B8%8A%E5%82%B3/%E4%B8%8B%E8%BC%89%E5%97%8E%EF%BC%9F)**
"""
    full = help_top + help_site + help_foot
    help_message = await userbot.send_message(channel, full, link_preview=False)
    await asyncio.sleep(90)
    try:
        await help_message.delete()
    except:
        pass


@userbot.on(events.NewMessage(pattern="/pthelp"))
async def generate_ptwiki_from_event(event) -> None:
    """generate pthelp based on event."""
    msg = event.message
    if (not msg.text) or (not msg.text.lower().startswith("/pthelp")):
        return
    to_chat = await event.get_chat()

    _, *rest = msg.text.lower().split(" ")

    if not rest:
        try:
            await msg.delete()

            nowtime = datetime.datetime.now()
            channelid = str(to_chat.id)
            if channelid in records:
                lasttime = records[channelid]
                delta = nowtime - lasttime
                if delta.total_seconds() < 80:
                    return
                records[channelid] = nowtime
            else:
                records[channelid] = nowtime

        except:
            pass
        await send_help(to_chat, event)
