

from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InputRichMessage

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


@MickeyBot.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    if query.data == "HELP":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=HELP_READ),
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    elif query.data == "CLOSE":
        await query.message.delete()
        await query.answer("ᴄʟᴏsᴇᴅ ᴍᴇɴᴜ!", show_alert=True)
    elif query.data == "BACK":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=START),
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
    elif query.data == "SOURCE":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=SOURCE_READ),
            reply_markup=InlineKeyboardMarkup(BACK),
        )
    elif query.data == "ABOUT":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=ABOUT_READ),
            reply_markup=InlineKeyboardMarkup(ABOUT_BTN),
        )
    elif query.data == "ADMINS":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=ADMIN_READ),
            reply_markup=InlineKeyboardMarkup(MUSIC_BACK_BTN),
        )
    elif query.data == "TOOLS_DATA":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=TOOLS_DATA_READ),
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif query.data == "BACK_HELP":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=HELP_READ),
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    elif query.data == "CHATBOT_CMD":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=CHATBOT_READ),
            reply_markup=InlineKeyboardMarkup(CHATBOT_BACK),
        )
    elif query.data == "CHATBOT_BACK":
        await query.message.edit_text(
            rich_message=InputRichMessage(html=HELP_READ),
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
    elif query.data == "addchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs!",
                show_alert=True,
            )
        is_vick = vick.find_one({"chat_id": query.message.chat.id})
        if not is_vick:
            await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            vick.delete_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(
                f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
            )
    elif query.data == "rmchat":
        user_id = query.from_user.id
        user_status = (await query.message.chat.get_member(user_id)).status
        if user_status not in [CMS.OWNER, CMS.ADMINISTRATOR]:
            return await query.answer(
                "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴇᴠᴇɴ ᴀɴ ᴀᴅᴍɪɴ, ᴅᴏɴ'ᴛ ᴛʀʏ ᴛʜɪs!",
                show_alert=True,
            )
        is_vick = vick.find_one({"chat_id": query.message.chat.id})
        if not is_vick:
            vick.insert_one({"chat_id": query.message.chat.id})
            await query.edit_message_text(
                f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}."
            )
        else:
            await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
