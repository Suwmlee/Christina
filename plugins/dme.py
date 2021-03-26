""" Module to automate message deletion. """
from asyncio import sleep
from os import path, remove, getcwd
from telethon import events, hints

@userbot.on(events.NewMessage(pattern="-dme"))
async def dme_from_event(event) -> None:
    """dme based on event."""
    msg = event.message
    user = await msg.get_sender()
    me = await userbot.get_me()

    if me.id != user.id:
        return

    if (not msg.text) or (not msg.text.lower().startswith("-dme")):
        return
    
    await dme(msg)


async def dme(context):
    """ Deletes specific amount of messages you sent. """
    try:
        count = int(context.text.split()[1]) + 1
    except ValueError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    except IndexError:
        await context.edit("出错了呜呜呜 ~ 无效的参数。")
        return
    dme_msg = " _(:з」∠)_ "
    count_buffer = 0
    async for message in userbot.iter_history(context.chat.id):
        if message.from_user.id == context.from_user.id:
            if count_buffer == count:
                break
            if message.forward_from or message.via_bot or message.sticker or message.contact \
                    or message.poll or message.game or message.location:
                pass
            elif message.text or message.voice:
                if not message.text == dme_msg:
                    try:
                        await message.edit(dme_msg)
                    except:
                        pass
            elif message.document or message.photo or message.audio or message.video or message.gif:
                if target_file:
                    if not message.text == dme_msg:
                        await message.edit(dme_msg)
                else:
                    if not message.text == dme_msg:
                        try:
                            await message.edit(dme_msg)
                        except:
                            pass
            else:
                pass
            await message.delete()
            count_buffer += 1
        else:
            pass
    count -= 1
    count_buffer -= 1
    notification = await send_prune_notify(userbot, context, count_buffer, count)
    await sleep(.5)
    await notification.delete()


async def send_prune_notify(client, context, count_buffer, count):
    return await client.send_message(
        context.chat.id,
        "删除了 "
        + str(count_buffer) + " / " + str(count)
        + " 条消息。"
    )
