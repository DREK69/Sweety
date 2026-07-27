import random
import re
import time
import asyncio
from pymongo import MongoClient, ASCENDING
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS, ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, Message
from config import MONGO_URL
from Mickey import MickeyBot
from Mickey.database.chats import add_served_chat, remove_served_chat
from Mickey.database.users import add_served_user
from Mickey.modules.helpers import CHATBOT_ON
from Mickey.modules.helpers.moderation import is_toxic

_mongo = MongoClient(MONGO_URL)
chatai = _mongo["Word"]["WordDb"]
vick = _mongo["VickDb"]["Vick"]
reactions_db = _mongo["Reactions"]["ReactionsDb"]

chatai.create_index("norm")
chatai.create_index([("chat_id", ASCENDING), ("norm", ASCENDING)])

REACTION_EMOJIS = ["❤️", "🔥", "😁", "👍", "😂", "😮"]
COOLDOWN_SECONDS = 3

LAST_REPLY_TIME = {}
LAST_RESPONSE = {}


COMMAND_PREFIXES = ("!", "/", "?", "@", "#")


def is_command(text) -> bool:
    if not text:
        return False
    return str(text).startswith(COMMAND_PREFIXES)


def reactions_enabled(chat_id: int) -> bool:
    return bool(reactions_db.find_one({"chat_id": chat_id}))


def normalize(text) -> str:
    return re.sub(r"\s+", " ", str(text).strip()).lower()


@MickeyBot.on_cmd("chatbot")
async def chaton_(_, m: Message):
    if m.chat.type != ChatType.PRIVATE:
        member = await m.chat.get_member(m.from_user.id)
        if member.status not in (CMS.OWNER, CMS.ADMINISTRATOR):
            return await m.reply_text("**ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.**")

    chat_label = "your private chat" if m.chat.type == ChatType.PRIVATE else m.chat.title
    await m.reply_text(
        f"ᴄʜᴀᴛ: {chat_label}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
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
            {
                "chat_id": message.chat.id,
                "trigger": trigger,
                "response": response,
                "norm": normalize(trigger),
            }
        )


async def _lookup_and_respond(client: Client, message: Message, chat_scoped: bool):
    if is_command(message.text):
        return

    now = time.monotonic()
    if now - LAST_REPLY_TIME.get(message.chat.id, 0) < COOLDOWN_SECONDS:
        return

    norm = normalize(message.text)

    if chat_scoped:
        matches = await asyncio.to_thread(
            lambda: list(chatai.find({"norm": norm, "chat_id": message.chat.id}).limit(30))
        )
        if not matches:
            matches = await asyncio.to_thread(
                lambda: list(chatai.find({"norm": norm, "chat_id": None}).limit(30))
            )
    else:
        matches = await asyncio.to_thread(
            lambda: list(chatai.find({"norm": norm}).limit(30))
        )

    if not matches:
        return

    last_response = LAST_RESPONSE.get(message.chat.id)
    pool = [m for m in matches if m["response"] != last_response] or matches
    random.shuffle(pool)
    candidates = pool[:5]

    toxic_flags = await asyncio.gather(*(is_toxic(c["response"]) for c in candidates))
    pick = next((c for c, flag in zip(candidates, toxic_flags) if not flag), None)
    if not pick:
        return

    # Reserve the cooldown slot now, before any network calls. Otherwise two
    # messages arriving in the same chat milliseconds apart can both pass the
    # cooldown check above and race each other into a double send.
    LAST_REPLY_TIME[message.chat.id] = time.monotonic()

    delay = min(0.4 + len(pick["response"]) * 0.03, 3.0)

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    except Exception:
        pass

    await asyncio.sleep(delay)

    try:
        await message.reply_text(pick["response"])
    except FloodWait as e:
        wait = e.value or 0
        if wait > 10:
            return
        await asyncio.sleep(wait)
        try:
            await message.reply_text(pick["response"])
        except Exception:
            return
    except Exception:
        return

    LAST_RESPONSE[message.chat.id] = pick["response"]

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
    replied = message.reply_to_message
    if replied and not (replied.from_user and replied.from_user.is_self):
        return
    if vick.find_one({"chat_id": message.chat.id}):
        return
    await _lookup_and_respond(client, message, chat_scoped=True)


@MickeyBot.on_message(
    filters.private & filters.text & ~filters.bot,
    group=5,
)
async def pvt_reply(client: Client, message: Message):
    if vick.find_one({"chat_id": message.chat.id}):
        return
    await _lookup_and_respond(client, message, chat_scoped=False)


@MickeyBot.on_message(filters.group, group=-1)
async def track_chat(_, message: Message):
    await add_served_chat(message.chat.id)


@MickeyBot.on_message(filters.private, group=-1)
async def track_user(_, message: Message):
    if message.from_user:
        await add_served_user(message.from_user.id)


@MickeyBot.on_chat_member_updated()
async def on_bot_membership_change(_, cmu: ChatMemberUpdated):
    if not cmu.new_chat_member or not cmu.new_chat_member.user.is_self:
        return

    status = cmu.new_chat_member.status
    if status in (CMS.LEFT, CMS.BANNED):
        await remove_served_chat(cmu.chat.id)
    elif status in (CMS.MEMBER, CMS.ADMINISTRATOR):
        await add_served_chat(cmu.chat.id)
        
