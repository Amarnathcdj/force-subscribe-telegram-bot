# porting to lawda by @terrorak...
# i asked rekcah before porting...not like other kangers....
# keep credit if u wanna kang...
# else u are a gay...no doubt in that....

# --------------------------------------------------------------------------------------------------------------------------------

from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from Luna import abot, tbot, ubot
from Luna.events import register
client = abot
async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.abot(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.abot(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@register(pattern="^/kid ?(.*)")
async def get_users(event):
    hell = await event.reply("`processing to kidnapp...`")
    kraken = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await hell.edit("`Sorry, kidnapp users here`")
    s = 0
    f = 0
    error = "None"

    await hell.edit("♤KidnappedStatus♤\n\n`Kidnaping Users.......`")
    async for user in event.abot.iter_participants(kraken.full_chat.id):
        try:
            if error.startswith("Too"):
                return await hell.edit(
                    f"**Kidnapping Finished With Error**\n(`May Got Limit Error from kidnaper lol, Please try again Later`)\n**Error** : \n`{error}`\n\n• Kidnapped `{s}` people \n• Failed to Kidnapp `{f}` people"
                )
            await event.abot(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await hell.edit(
                f"**Kidnapping Running...**\n\n• Kidnapped `{s}` people \n• Failed to Kidnapp `{f}` people\n\n**× LastError:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await hell.edit(
        f"**Kidnapping Finished** \n\n• Successfully Kidnapped `{s}` people \n• failed to Kidnapp `{f}` people"
    )
