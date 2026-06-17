import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_NAME = os.getenv("OWNER_NAME")
OWNER_ID_ENV = os.getenv("OWNER_ID")

if not all([BOT_TOKEN, OWNER_NAME, OWNER_ID_ENV]):
    logger.critical("Missing required environment variables (BOT_TOKEN, OWNER_NAME, OWNER_ID).")
    exit(1)

try:
    OWNER_ID = int(OWNER_ID_ENV)
except ValueError:
    logger.critical("OWNER_ID must be a valid integer.")
    exit(1)

blocked_users = set()

STRINGS = {
    "en": {
        "owner_welcome": (
            "👋 Hello {owner_name}!\n\n"
            "Owner commands:\n"
            "• `/reply <user_id> <message>`\n"
            "• `/block <user_id>`\n"
            "• `/unblock <user_id>`\n"
            "• `/blocked`"
        ),
        "user_welcome": "Hi! You've reached {owner_name}'s assistant. Send your message and you'll get a reply soon. 👋",
        "reply_usage": "⚠️ Usage: /reply <user_id> <message>",
        "invalid_id": "❌ Invalid User ID.",
        "reply_success": "✅ Message sent to {name}",
        "reply_failed": "❌ Could not send message",
        "block_usage": "⚠️ Usage: /block <user_id>",
        "block_success": "🚫 User {blocked_id} has been blocked.",
        "unblock_usage": "⚠️ Usage: /unblock <user_id>",
        "unblock_success": "✅ User {unblocked_id} has been unblocked.",
        "unblock_not_found": "ℹ️ User {unblocked_id} is not blocked.",
        "blocked_empty": "ℹ️ No blocked users.",
        "blocked_list": "🚫 *Blocked Users:*\n{list}",
        "user_received": "✅ Message received! You'll get a reply soon.",
        "msg_label_name": "👤 Name: {name}",
        "msg_label_username": "🔗 Username: @{username}",
        "msg_label_id": "🆔 User ID: {user_id}",
        "msg_forward_header": "📩 New message from:",
        "msg_media_header": "📩 New media from:",
        "msg_label_message": "💬 Message:",
        "msg_label_to_reply": "➡️ To reply: /reply {user_id} [your message]",
    },
    "ar": {
        "owner_welcome": (
            "👋 مرحبًا {owner_name}!\n\n"
            "أوامر المالك المتاحة:\n"
            "• `/reply <user_id> <message>` - الرد على رسالة\n"
            "• `/block <user_id>` - حظر مستخدم\n"
            "• `/unblock <user_id>` - إلغاء حظر\n"
            "• `/blocked` - عرض المحظورين"
        ),
        "user_welcome": "مرحبًا! لقد وصلت إلى مساعد {owner_name}. أرسل رسالتك وسنرد عليك قريبًا. 👋",
        "reply_usage": "⚠️ الاستخدام: /reply <user_id> <الرسالة>",
        "invalid_id": "❌ معرف مستخدم غير صحيح.",
        "reply_success": "✅ تم إرسال الرسالة إلى {name}",
        "reply_failed": "❌ تعذر إرسال الرسالة",
        "block_usage": "⚠️ الاستخدام: /block <user_id>",
        "block_success": "🚫 تم حظر المستخدم {blocked_id}.",
        "unblock_usage": "⚠️ الاستخدام: /unblock <user_id>",
        "unblock_success": "✅ تم إلغاء حظر المستخدم {unblocked_id}.",
        "unblock_not_found": "ℹ️ المستخدم {unblocked_id} ليس في القائمة.",
        "blocked_empty": "ℹ️ لا يوجد مستخدمون محظورون.",
        "blocked_list": "🚫 *المستخدمين المحظورين:*\n{list}",
        "user_received": "✅ تم استلام رسالتك! ستتلقى ردًا قريبًا.",
        "msg_label_name": "👤 الاسم: {name}",
        "msg_label_username": "🔗 اسم المستخدم: @{username}",
        "msg_label_id": "🆔 معرف المستخدم: {user_id}",
        "msg_forward_header": "📩 رسالة جديدة من:",
        "msg_media_header": "📩 وسائط جديدة من:",
        "msg_label_message": "💬 الرسالة:",
        "msg_label_to_reply": "➡️ للرد: /reply {user_id} [رسالتك]",
    },
}


def get_lang(user) -> str:
    if user and user.language_code and user.language_code.startswith("ar"):
        return "ar"
    return "en"


def t(user, key: str, **kwargs) -> str:
    lang = get_lang(user)
    text = STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, ""))
    return text.format(**kwargs) if kwargs else text


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    if user.id == OWNER_ID:
        await update.message.reply_text(t(user, "owner_welcome", owner_name=OWNER_NAME), parse_mode=ParseMode.MARKDOWN)
        return

    if user.id in blocked_users:
        return

    await update.message.reply_text(t(user, "user_welcome", owner_name=OWNER_NAME))


async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    parts = update.message.text.split(None, 2)
    if len(parts) < 3:
        await update.message.reply_text(t(update.effective_user, "reply_usage"))
        return

    user_id_str, msg_text = parts[1], parts[2]
    if not user_id_str.isdigit():
        await update.message.reply_text(t(update.effective_user, "invalid_id"))
        return

    uid = int(user_id_str)
    try:
        chat = await context.bot.get_chat(chat_id=uid)
        name = chat.first_name or f"User {uid}"
        await context.bot.send_message(chat_id=uid, text=msg_text)
        await update.message.reply_text(t(update.effective_user, "reply_success", name=name))
    except Exception as e:
        logger.error(f"Error sending reply to {uid}: {e}")
        await update.message.reply_text(t(update.effective_user, "reply_failed"))


async def block_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(t(update.effective_user, "block_usage"))
        return

    uid = int(context.args[0])
    blocked_users.add(uid)
    await update.message.reply_text(t(update.effective_user, "block_success", blocked_id=uid))


async def unblock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(t(update.effective_user, "unblock_usage"))
        return

    uid = int(context.args[0])
    if uid in blocked_users:
        blocked_users.remove(uid)
        await update.message.reply_text(t(update.effective_user, "unblock_success", unblocked_id=uid))
    else:
        await update.message.reply_text(t(update.effective_user, "unblock_not_found", unblocked_id=uid))


async def blocked_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user or update.effective_user.id != OWNER_ID:
        return

    if not blocked_users:
        await update.message.reply_text(t(update.effective_user, "blocked_empty"))
        return

    lst = "\n".join(f"• `{u}`" for u in blocked_users)
    await update.message.reply_text(t(update.effective_user, "blocked_list", list=lst), parse_mode=ParseMode.MARKDOWN)


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return

    user = update.effective_user
    if user.id == OWNER_ID or user.id in blocked_users:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(1)

    name = user.first_name or "User"
    uname = user.username
    uid = user.id

    uname_str = t(user, "msg_label_username", username=uname) + "\n" if uname else ""
    info = f"{t(user, 'msg_label_name', name=name)}\n{uname_str}{t(user, 'msg_label_id', user_id=uid)}"
    reply_hint = t(user, "msg_label_to_reply", user_id=uid)

    try:
        if update.message.text:
            msg = f"{t(user, 'msg_forward_header')}\n{info}\n\n{t(user, 'msg_label_message')}\n{update.message.text}\n\n{reply_hint}"
            await context.bot.send_message(chat_id=OWNER_ID, text=msg)
        else:
            header = f"{t(user, 'msg_media_header')}\n{info}\n\n{reply_hint}"
            await context.bot.send_message(chat_id=OWNER_ID, text=header)
            await update.message.forward(chat_id=OWNER_ID)

        await update.message.reply_text(t(user, "user_received"))
    except Exception as e:
        logger.error(f"Error handling msg from {uid}: {e}")


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update failed:", exc_info=context.error)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("reply", reply_cmd))
    app.add_handler(CommandHandler("block", block_cmd))
    app.add_handler(CommandHandler("unblock", unblock_cmd))
    app.add_handler(CommandHandler("blocked", blocked_cmd))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, on_message))
    app.add_error_handler(handle_error)

    logger.info("Service started...")
    app.run_polling()


if __name__ == "__main__":
    main()
