#!/usr/bin/env python3

import certifi
import ssl
from asyncio import sleep
from os import remove
from urllib import request
from io import BytesIO
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from telethon.errors.common import AlreadyInConversationError
from PIL import Image
from math import floor
from telethon import events, hints


@userbot.on(events.NewMessage(pattern="-add"))
async def sticker(event):
    """ Fetches images/stickers and add them to your pack. """
    context = event.message
    user = await userbot.get_me()
    sender = await context.get_sender()

    if sender.id != user.id:
        return

    if (not context.text) or (not context.text.lower().startswith("-add")):
        return

    _, *rest = context.text.lower().split(" ")
    if rest:
        return

    if not user.username:
        user.username = user.first_name
    message = await context.get_reply_message()
    custom_emoji = False
    animated = False
    emoji = ""
    try:
        await context.edit("收集图像/贴纸中 . . .")
    except:
        pass
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            photo = BytesIO()
            photo = await userbot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split('/'):
            photo = BytesIO()
            try:
                await context.edit("下载图片中 . . .")
            except:
                pass
            await userbot.download_file(message.media.document, photo)
            if (DocumentAttributeFilename(file_name='sticker.webp') in
                    message.media.document.attributes):
                emoji = message.media.document.attributes[1].alt
                custom_emoji = True
        elif (DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in
              message.media.document.attributes):
            photo = BytesIO()
            await userbot.download_file(message.media.document, "AnimatedSticker.tgs")
            for index in range(len(message.media.document.attributes)):
                try:
                    emoji = message.media.document.attributes[index].alt
                    break
                except:
                    pass
            custom_emoji = True
            animated = True
            photo = 1
        else:
            try:
                await context.edit("`出错了呜呜呜 ~ 不支持此文件类型。`")
            except:
                pass
            return
    else:
        try:
            await context.edit("`出错了呜呜呜 ~ 请回复带有图片/贴纸的消息。`")
        except:
            pass
        return

    if photo:
        split_strings = context.text.split()
        if not custom_emoji:
            emoji = "👀"
        pack = 1
        sticker_already = False
        if len(split_strings) == 3:
            pack = split_strings[2]
            emoji = split_strings[1]
        elif len(split_strings) == 2:
            if split_strings[1].isnumeric():
                pack = int(split_strings[1])
            else:
                emoji = split_strings[1]

        pack_name = "tg_matches"
        pack_title = "water~water~"
        command = '/newpack'
        file = BytesIO()

        if not animated:
            try:
                await context.edit("调整图像大小中 . . .")
            except:
                pass
            image = await resize_image(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            pack_name += "_animated"
            pack_title += " (animated)"
            command = '/newanimated'

        response = request.urlopen(
            request.Request(f'http://t.me/addstickers/{pack_name}'), context=ssl.create_default_context(cafile=certifi.where()))
        if not response.status == 200:
            try:
                await context.edit("连接到 Telegram 服务器失败 . . .")
            except:
                pass
            return
        http_response = response.read().decode("utf8").split('\n')

        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in \
                http_response:
            for _ in range(20):  # 最多重试20次
                try:
                    async with userbot.conversation('Stickers') as conversation:
                        await conversation.send_message('/addsticker')
                        await conversation.get_response()
                        await userbot.send_read_acknowledge(conversation.chat_id)
                        await conversation.send_message(pack_name)
                        chat_response = await conversation.get_response()
                        while chat_response.text == "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment.":
                            pack += 1
                            pack_name = f"tg_matches_{pack}"
                            pack_title = f"water~water~ {pack}"
                            try:
                                await context.edit("切换到私藏 " + str(pack) + " 上一个贴纸包已满 . . .")
                            except:
                                pass
                            await conversation.send_message(pack_name)
                            chat_response = await conversation.get_response()
                            if chat_response.text == "Invalid pack selected.":
                                await add_sticker(conversation, command, pack_title, pack_name, animated, message,
                                                  context, file, emoji)
                                try:
                                    await context.edit(
                                        f"这张图片/贴纸已经被添加到 [这个](t.me/addstickers/{pack_name}) 贴纸包。",
                                        parse_mode='md')
                                except:
                                    pass
                                return
                        await upload_sticker(animated, message, context, file, conversation)
                        await conversation.get_response()
                        await conversation.send_message(emoji)
                        await userbot.send_read_acknowledge(conversation.chat_id)
                        await conversation.get_response()
                        await conversation.send_message('/done')
                        await conversation.get_response()
                        await userbot.send_read_acknowledge(conversation.chat_id)
                        break
                except AlreadyInConversationError:
                    if not sticker_already:
                        try:
                            await context.edit("另一个命令正在添加贴纸, 重新尝试中")
                        except:
                            pass
                        sticker_already = True
                    else:
                        pass
                    await sleep(.5)
                except Exception:
                    raise
        else:
            try:
                await context.edit("贴纸包不存在，正在创建 . . .")
            except:
                pass
            async with userbot.conversation('Stickers') as conversation:
                await add_sticker(conversation, command, pack_title, pack_name, animated, message,
                                  context, file, emoji)

        try:
            await context.edit(
                f"这张图片/贴纸已经被添加到 [这个](t.me/addstickers/{pack_name}) 贴纸包。",
                parse_mode='md')
        except:
            pass
        await sleep(5)
        try:
            await context.delete()
        except:
            pass


async def add_sticker(conversation, command, pack_title, pack_name, animated, message, context, file, emoji):
    await conversation.send_message(command)
    await conversation.get_response()
    await userbot.send_read_acknowledge(conversation.chat_id)
    await conversation.send_message(pack_title)
    await conversation.get_response()
    await userbot.send_read_acknowledge(conversation.chat_id)
    await upload_sticker(animated, message, context, file, conversation)
    await conversation.get_response()
    await conversation.send_message(emoji)
    await userbot.send_read_acknowledge(conversation.chat_id)
    await conversation.get_response()
    await conversation.send_message("/publish")
    if animated:
        await conversation.get_response()
        await conversation.send_message(f"<{pack_title}>")
    await conversation.get_response()
    await userbot.send_read_acknowledge(conversation.chat_id)
    await conversation.send_message("/skip")
    await userbot.send_read_acknowledge(conversation.chat_id)
    await conversation.get_response()
    await conversation.send_message(pack_name)
    await userbot.send_read_acknowledge(conversation.chat_id)
    await conversation.get_response()
    await userbot.send_read_acknowledge(conversation.chat_id)


async def upload_sticker(animated, message, context, file, conversation):
    if animated:
        try:
            await context.edit("上传动图中 . . .")
        except:
            pass
        await conversation.send_file("AnimatedSticker.tgs", force_document=True)
        remove("AnimatedSticker.tgs")
    else:
        file.seek(0)
        try:
            await context.edit("上传图片中 . . .")
        except:
            pass
        await conversation.send_file(file, force_document=True)


async def resize_image(photo):
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = floor(size1new)
        size2new = floor(size2new)
        size_new = (size1new, size2new)
        image = image.resize(size_new)
    else:
        image.thumbnail(maxsize)

    return image
