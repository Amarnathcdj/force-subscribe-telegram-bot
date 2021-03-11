from Luna import CMD_HELP, OWNER_ID
from Luna.events import register
import os

k = 'News Py Files In Another Repo'
@register(pattern="^/teg ?(.*)")
async def sleepybot(time):
    if time.fwd_from:
        return
    if time.sender_id == OWNER_ID:
        pass
    else:
        return
    await time.reply("Fed Py In App 2")


file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /newfed <fed_name>: Creates a Federation, one allowed per user.
 - /renamefed <fed_id> <new_fed_name>: Renames the fed id to a new name.
 - /delfed <fed_id>: Delete a Federation, and any information related to it. 
 - /fpromote <user>: Assigns the user as a federation admin. 
 - /fdemote <user>: Drops the user from the federation admin to a normal user.
 - /subfed <fed_id>: Subscribes to a given fed ID, fedbans from that subscribed fed will also happen in your fed
 - /unsubfed <fed_id>: Unsubscribes to a given fed ID
 - /setfedlog <fed_id>: Sets the group as a fed log report base for the federation
 - /unsetfedlog <fed_id>: Removed the group as a fed log report base for the federation
 - /fbroadcast <message>: Broadcasts a messages to all groups that have joined your fed
 - /fedsubs: Shows the feds your group is subscribed to (broken rn)
 - /fban (<user>|<reason>): Fed bans a user. Syntax: `fban 12345 | testing`, `fban @MissJuliaRobot | testing`.
 - /unfban <user> <reason>: Removes a user from a fed ban.
 - /fedinfo <fed_id>: Information about the specified Federation.
 - /joinfed <fed_id>: Join the current chat to the Federation. 
 - /leavefed <fed_id>: Leave the Federation given. 
 - /setfrules <rules>: Arrange Federation rules.
 - /fedadmins: Show Federation admin.
 - /fbanlist: Displays all users who are victimized at the Federation at this time.
 - /fedchats: Get all the chats that are connected in the Federation.
 - /chatfed : See the Federation in the current chat.
 - /fbanstat: Shows if you/or the user you are replying to or their username/id is fbanned somewhere or not.
 - /fednotif <on/off>: Should the bot send notifications for fban/unfban in PM.
 - /frules: See the current federation rules.
 - /exportfbans: Returns a list of all banned users in the current federation.
 - /importfbans: Imports all fbanned uses from the export file into the current chat federation.

**NOTE**: Federation ban doesn't ban the user from the fed chats instead kicks everytime they join the chat.
"""

CMD_HELP.update({file_helpo: [file_helpo, __help__]})
