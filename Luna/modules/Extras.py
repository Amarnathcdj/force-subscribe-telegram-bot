from Luna import tbot, CMD_HELP
import os
from Luna.events import register
import secureme

@register(pattern="^/encrypt ?(.*)")
async def hmm(event):
    if event.reply_to_msg_id:
          lel = await event.get_reply_message()
          cmd = lel.text
    else:
          cmd = event.pattern_match.group(1)
    Text = cmd
    k = secureme.encrypt(Text)
    await event.reply(k)

@register(pattern="^/decrypt ?(.*)")
async def hmm(event):
    if event.reply_to_msg_id:
          lel = await event.get_reply_message()
          ok = lel.text
    else:
          ok = event.pattern_match.group(1)
    Text = ok
    k = secureme.decrypt(Text)
    await event.reply(k)

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /cash : currency converter
Example syntax: `/cash 1 USD INR`
 - /crypto : Crypto Value
Example syntax: `/crypto inr btc`
 - /country: Gather's Info About The Given Country
 - /encrypt: Encrypts The Given Text
 - /decrypt: Decrypts Previously Ecrypted Text
 - /google: Performs A Google Search With given Query
 - /img: Search Google for images and returns them\nFor greater no. of results specify lim, For eg: `/img hello lim=10`
 - /reverse: Does a reverse image search of the media which it was replied to
 - @AniegrpBot yt <query>: Inline YouTube Search
 - q <query>: Answers meaning full questions
 - /quote: Sends quotes of famous personalities
 - /t(m|text): Reply to a message to get a permanent telegra.ph link.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
