from pyrogram.enums import ChatMemberStatus as CMS, ChatType, ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

try:
    from pyrogram.types import InputRichMessage
    RICH_SUPPORTED = True
except ImportError:
    RICH_SUPPORTED = False

from Mickey import MickeyBot
from Mickey.database import vick
from Mickey.modules.helpers import (
    ABOUT_BTN,
    ABOUT_READ,
    ADMIN_READ,
    BACK,
    CHATBOT_BACK,
    CHATBOT_READ,
    CHATBOT_RICH_HTML,
    DEV_OP,
    HELP_BTN,
    HELP_READ,
    HELP_RICH_HTML,
    MUSIC_BACK_BTN,
    SOURCE_READ,
    START,
    TOOLS_DATA_READ,
    TOOLS_RICH_HTML,
)

TEXT_ROUTES = {
    "HELP": (HELP_READ, HELP_RICH_HTML, HELP_BTN),
    "BACK": (START, None, DEV_OP),
    "SOURCE": (SOURCE_READ, None, BACK),
    "ABOUT": (ABOUT_READ, None, ABOUT_BTN),
    "ADMINS": (ADMIN_READ, None, MUSIC_BACK_BTN),
    "TOOLS_DATA": (TOOLS_DATA_READ, TOOLS_RICH_HTML, CHATBOT_BACK),
    "BACK_HELP": (HELP_READ, HELP_RICH_HTML, HELP_BTN),
    "CHATBOT_CMD": (CHATBOT_READ, CHATBOT_RICH_HTML, CHATBOT_BACK),
    "CHATBOT_BACK": (HELP_READ, HELP_RICH_HTML, HELP_BTN),
}


async def _render(query, plain_text, rich_html, buttons):
    markup = InlineKeyboardMarkup(buttons)

    if RICH_SUPPORTED and rich_html:
        try:
            return await query.message.edit_text(
                rich_message=InputRichMessage(html=rich_html),
                reply_markup=markup,
            )
        except TypeError:
            pass

    return await query.message.edit_text(
        plain_text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup,
        disable_web_page_preview=True,
    )


@MickeyBot.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    data = query.data

    if data == "CLOSE":
        await query.message.delete()
        return await query.answer("ᴄʟᴏsᴇᴅ ᴍᴇɴᴜ!", show_alert=True)

    if data in TEXT_ROUTES:
        text, rich_html, buttons = TEXT_ROUTES[data]
        return await _render(query, text, rich_html, buttons)

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
                
