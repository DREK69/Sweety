import random

from Abg import adminsOnly
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS, ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

from config import MONGO_URL
from Mickey import MickeyBot
from Mickey.modules.helpers import CHATBOT_ON, is_admins
from Mickey.modules.helpers.moderation import is_toxic

_mongo = MongoClient(MONGO_URL)
chatai = _mongo["Word"]["WordDb"]
vick = _mongo["VickDb"]["Vick"]
reactions_db = _mongo["Reactions"]["ReactionsDb"]

REACTION_EMOJIS = ["❤️", "🔥", "😁", "👍", "😂", "😮"]


def is_command(text: str) -> bool:
    if not text:
        return False
    return text[0] in "!/?@#"


def reactions_enabled(chat_id: int) -> bool:
    return bool(reactions_db.find_one({"chat_id": chat_id}))


@MickeyBot.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


@MickeyBot.on_cmd("reaction")
async def reaction_toggle(_, m: Message):
    if m.chat.type != ChatType.PRIVATE:
        member = await m.chat.get_member(m.from_user.id)
        if member.status not in (CMS.OWNER, CMS.ADMINISTRATOR):
            return await m.reply_text("**ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")

    args = m.text.split(None, 1)
    if len(args) < 2 or args[1].strip().lower() not in ("on", "off"):
        return await m.reply_text("**ᴜsᴀɢᴇ:** /reaction [on/off]")

    mode = args[1].strip().lower()
    if mode == "on":
        if not reactions_enabled(m.chat.id):
            reactions_db.insert_one({"chat_id": m.chat.id})
        await m.reply_text("**ʀᴇᴀᴄᴛɪᴏɴs ᴇɴᴀʙʟᴇᴅ.**")
    else:
        reactions_db.delete_one({"chat_id": m.chat.id})
        await m.reply_text("**ʀᴇᴀᴄᴛɪᴏɴs ᴅɪsᴀʙʟᴇᴅ.**")


@MickeyBot.on_message(
    filters.group & filters.text & ~filters.via_bot & ~filters.bot,
    group=4,
)
async def teach_reply(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return
    if is_command(message.text) or is_command(message.reply_to_message.text):
        return

    trigger = message.reply_to_message.text
    response = message.text

    if await is_toxic(trigger) or await is_toxic(response):
        return

    exists = chatai.find_one(
        {"trigger": trigger, "response": response, "chat_id": message.chat.id}
    )
    if not exists:
        chatai.insert_one(
            {"chat_id": message.chat.id, "trigger": trigger, "response": response}
        )


async def _lookup_and_respond(client: Client, message: Message, chat_scoped: bool):
    if is_command(message.text):
        return

    query = {"trigger": message.text}
    if chat_scoped:
        query["chat_id"] = message.chat.id

    matches = list(chatai.find(query))
    if not matches:
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    pick = random.choice(matches)
    await message.reply_text(pick["response"])

    if reactions_enabled(message.chat.id):
        try:
            await message.react(random.choice(REACTION_EMOJIS))
        except Exception:
            pass


@MickeyBot.on_message(
    filters.group & filters.text & ~filters.via_bot & ~filters.bot,
    group=5,
)
async def auto_reply(client: Client, message: Message):
    if message.reply_to_message:
        return
    if vick.find_one({"chat_id": message.chat.id}):
        return
    await _lookup_and_respond(client, message, chat_scoped=True)


@MickeyBot.on_message(
    filters.private & filters.text & ~filters.bot,
    group=5,
)
async def pvt_reply(client: Client, message: Message):
    await _lookup_and_respond(client, message, chat_scoped=False)
    
