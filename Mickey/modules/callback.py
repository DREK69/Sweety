from pyrogram.enums import ChatMemberStatus as CMS, ChatType, ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from Mickey import MickeyBot
from Mickey.database import vick
from Mickey.modules.helpers import (
    ABOUT_BTN,
    ABOUT_READ,
    ADMIN_READ,
    BACK,
    CHATBOT_BACK,
    CHATBOT_READ,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    MUSIC_BACK_BTN,
    SOURCE_READ,
    START,
    TOOLS_DATA_READ,
)

TEXT_ROUTES = {
    "HELP": (HELP_READ, HELP_BTN),
    "BACK": (START, DEV_OP),
    "SOURCE": (SOURCE_READ, BACK),
    "ABOUT": (ABOUT_READ, ABOUT_BTN),
    "ADMINS": (ADMIN_READ, MUSIC_BACK_BTN),
    "TOOLS_DATA": (TOOLS_DATA_READ, CHATBOT_BACK),
    "BACK_HELP": (HELP_READ, HELP_BTN),
    "CHATBOT_CMD": (CHATBOT_READ, CHATBOT_BACK),
    "CHATBOT_BACK": (HELP_READ, HELP_BTN),
}


@MickeyBot.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    data = query.data

    if data == "CLOSE":
        await query.message.delete()
        return await query.answer("ᴄʟᴏsᴇᴅ ᴍᴇɴᴜ!", show_alert=True)

    if data in TEXT_ROUTES:
        text, buttons = TEXT_ROUTES[data]
        return await query.message.edit_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )

    if data in ("addchat", "rmchat"):
        chat = query.message.chat
        if chat.type != ChatType.PRIVATE:
            status = (await chat.get_member(query.from_user.id)).status
            if status not in (CMS.OWNER, CMS.ADMINISTRATOR):
                return await query.answer(
                    "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs!",
                    show_alert=True,
                )

        is_disabled = bool(vick.find_one({"chat_id": chat.id}))

        if data == "addchat":
            if not is_disabled:
                await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
            else:
                vick.delete_one({"chat_id": chat.id})
                await query.edit_message_text(
                    f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
                )
        else:
            if not is_disabled:
                vick.insert_one({"chat_id": chat.id})
                await query.edit_message_text(
                    f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
                )
            else:
                await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
                
