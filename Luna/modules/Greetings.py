import os
from telethon import events
from telethon.utils import pack_bot_file_id
from Luna.events import register
from Luna import tbot, CMD_HELP
from Luna.modules.sql.welcome_sql import (
    add_welcome_setting,
    get_current_welcome_settings,
    rm_welcome_setting,
    update_previous_welcome,
)
from Luna.modules.sql.welcome_sql import (
    add_goodbye_setting,
    get_current_goodbye_settings,
    rm_goodbye_setting,
    update_previous_goodbye,
)
import Luna.modules.sql.rules_sql as sql
from telethon import *
from telethon.tl import *
from Luna import *
import random
from telethon.tl.functions.channels import EditBannedRequest
from pymongo import MongoClient
from telethon.tl.types import ChatBannedRights

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
botcheck = db.checkbot
verified_user = db.user_verified

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    print(e)  # pylint:disable=E0602
            current_saved_welcome_message = cws.custom_welcome_message
            current_message = await event.reply(
                    current_saved_welcome_message,
                    file=cws.media_file_id,
                )
                update_previous_welcome(event.chat_id, current_message.id)

            
                

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # print("yo")
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        # print("gotcha")
        # print(event.stringify())
        """user_added=False,
        user_joined=False,
        user_left=True,
        user_kicked=True,"""
        if event.user_kicked or event.user_left:
            # print ("1")
            if cws.should_clean_goodbye:
                # print ("2")
                try:
                    await tbot.delete_messages(  # pylint:disable=E0602
                        event.chat_id, cws.previous_goodbye
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    print(e)  # pylint:disable=E0602
            # print ("3")
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await tbot.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            userid = a_user.id
            current_saved_goodbye_message = cws.custom_goodbye_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            # print(current_saved_goodbye_message)
            current_message = await event.reply(
                current_saved_goodbye_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    userid=userid,
                ),
                file=cws.media_file_id,
            )
            # print (current_message)
            update_previous_goodbye(event.chat_id, current_message.id)


# -- @MissJulia_Robot (sassiet captcha ever) --#




@register(pattern="^/setwelcome")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, False, 0, tbot_api_file_id)
        await event.reply("Welcome message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], False, 0, None)
        await event.reply("Welcome message saved. ")


@register(pattern="^/clearwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.reply(
        "Welcome message cleared. "
        + "The previous welcome message was `{}`".format(cws.custom_welcome_message)
    )


@register(pattern="^/checkwelcome$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, "custom_welcome_message"):
        await event.reply(
            "This chat's welcome message is\n\n`{}`".format(cws.custom_welcome_message)
        )
    else:
        await event.reply("No welcome message found for this chat")


@register(pattern="^/setgoodbye")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        tbot_api_file_id = pack_bot_file_id(msg.media)
        add_goodbye_setting(event.chat_id, msg.message, False, 0, tbot_api_file_id)
        await event.reply("Goodbye message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_goodbye_setting(event.chat_id, input_str[1], False, 0, None)
        await event.reply("Goodbye message saved. ")


@register(pattern="^/cleargoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_goodbye_settings(event.chat_id)
    rm_goodbye_setting(event.chat_id)
    await event.reply(
        "Goodbye message cleared. "
        + "The previous goodbye message was `{}`".format(cws.custom_goodbye_message)
    )


@register(pattern="^/checkgoodbye$")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if hasattr(cws, "custom_goodbye_message"):
        await event.reply(
            "This chat's goodbye message is\n\n`{}`".format(cws.custom_goodbye_message)
        )
    else:
        await event.reply("No goodbye message found for this chat")


@register(pattern="^/welcomecaptcha(?: |$)(.*)")
async def welcome_verify(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = botcheck.find({})
    if not input:
        for c in chats:
            if event.chat_id == c["id"]:
                await event.reply(
                    "Please provide some input yes or no.\n\nCurrent setting is : **on**"
                )
                return
        await event.reply(
            "Please provide some input yes or no.\n\nCurrent setting is : **off**"
        )
        return
    if input in "on":
        if event.is_group:
            chats = botcheck.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Welcome Captcha is already enabled for this chat."
                    )
                    return
            botcheck.insert_one({"id": event.chat_id})
            await event.reply("Welcome Captcha enabled for this chat.")
    if input in "off":
        if event.is_group:
            chats = botcheck.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    botcheck.delete_one({"id": event.chat_id})
                    await event.reply("Welcome Captcha disabled for this chat.")
                    return
        await event.reply("Welcome Captcha enabled for this chat.")

    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return


@register(pattern="^/cleanwelcome(?: |$)(.*)")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, "custom_welcome_message"):
        pass
    else:
        if input in "on":
            add_welcome_setting(event.chat_id, "", True, 0, None)
            await event.reply("I will clean old welcone messages from now.")
            return
        if input in "off":
            add_welcome_setting(event.chat_id, "", False, 0, None)
            await event.reply("I will not clean old welcone messages from now.")
            return
        if not input == "on" and not input == "off":
            await event.reply("I only understand by on or off")
            return
    mssg = cws.custom_welcome_message
    pvw = cws.previous_welcome
    mfid = cws.media_file_id
    if cws.should_clean_welcome is True:
        await event.reply("I am already cleaning old welcone messages.")
        return
    if input in "on":
        rm_welcome_setting(event.chat_id)
        add_welcome_setting(event.chat_id, mssg, True, pvw, mfid)
        await event.reply("I will clean old welcone messages from now.")
    if input in "off":
        rm_welcome_setting(event.chat_id)
        add_welcome_setting(event.chat_id, mssg, False, pvw, mfid)
        await event.reply("I will not clean old welcone messages from now.")
    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return


@register(pattern="^/cleangoodbye(?: |$)(.*)")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    cws = get_current_goodbye_settings(event.chat_id)
    if hasattr(cws, "custom_goodbye_message"):
        pass
    else:
        if input in "on":
            add_goodbye_setting(event.chat_id, "", True, 0, None)
            await event.reply("I will clean old welcone messages from now.")
            return
        if input in "off":
            add_goodbye_setting(event.chat_id, "", False, 0, None)
            await event.reply("I will not clean old welcone messages from now.")
            return
        if not input == "on" and not input == "off":
            await event.reply("I only understand by on or off")
            return
    mssg = cws.custom_goodbye_message
    pvw = cws.previous_goodbye
    mfid = cws.media_file_id
    if cws.should_clean_goodbye is True:
        await event.reply("I am already cleaning old welcone messages.")
        return
    if input in "on":
        rm_goodbye_setting(event.chat_id)
        add_goodbye_setting(event.chat_id, mssg, True, pvw, mfid)
        await event.reply("I will clean old welcone messages from now.")
    if input in "off":
        rm_goodbye_setting(event.chat_id)
        add_goodbye_setting(event.chat_id, mssg, False, pvw, mfid)
        await event.reply("I will not clean old welcone messages from now.")
    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
**Welcome**
 - /setwelcome <welcome message> or <reply to a text>: Saves the message as a welcome note in the chat.
 - /checkwelcome: Check whether you have a welcome note in the chat.
 - /clearwelcome: Deletes the welcome note for the current chat.
 - /welcomecaptcha <on/off>: Mutes a user on joining and unmutes as he/she solves a image captcha.
 - /cleanwelcome <on/off>: Clean previous welcome message before welcoming a new user

**Goodbye**
 - /setgoodbye <goodbye message> or <reply to a text>: Saves the message as a goodbye note in the chat.
 - /checkgoodbye: Check whether you have a goodbye note in the chat.
 - /cleargoodbye: Deletes the goodbye note for the current chat.
 - /cleangoodbye <on/off>: Clean previous goodbye message before farewelling a new user

**Available variables for formatting greeting message:**
`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`

**Note**: __You can't set new welcome/goodbye message before deleting the previous one.__
""" 
 
CMD_HELP.update({file_helpo: [file_helpo, __help__]})
