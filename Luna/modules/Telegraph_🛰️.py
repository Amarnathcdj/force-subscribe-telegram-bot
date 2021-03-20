from Luna import tbot, CMD_HELP
from Luna.events import register
import os
from datetime import datetime

dir = './'
from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

telegraph = Telegraph()
r = telegraph.create_account(Luna)
auth_url = r["auth_url"]


@register(pattern="^/t(m|t) ?(.*)")
async def tele(event):
   if event.fwd_from:
        return
   optional_title = event.pattern_match.group(2)
   if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "m":
            downloaded_file_name = await tbot.download_media(
                r_message, dir
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await event.reply("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                os.remove(downloaded_file_name)
                await event.reply(
                    "Uploaded to [Telegraph](https://telegra.ph{})".format(
                        media_urls[0]
                    ),
                    link_preview=False,
                )
        elif input_str == "t":
            user_object = await tbot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tbot.download_media(
                    r_message, dir
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            await event.edit(
                "Pasted to [Telegraph](https://telegra.ph/{})".format(
                    response["path"]
                ),
                link_preview=False,
            )
    else:
        await event.reply(
            "Reply to a message to get a permanent telegra.ph link."
        )
