import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatType, ChatMemberStatus, ParseMode
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatMemberUpdated,
    CallbackQuery,
)

import config
import database as db
from messages import AUTO_REPLY_TEXT, BUTTON_TEXT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# ---------- Yordamchi funksiyalar ----------

def contact_url() -> str:
    """'Habar berish' tugmasi ochadigan link."""
    if config.CONTACT_USERNAME:
        return f"https://t.me/{config.CONTACT_USERNAME}"
    return f"tg://user?id={config.CONTACT_ID}"


def reply_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=BUTTON_TEXT, url=contact_url())]]
    )


def admin_refresh_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_stats")]]
    )


async def stats_text() -> str:
    s = await db.get_stats()
    return (
        "📊 <b>Admin panel</b>\n\n"
        f"👥 Jami javob berilgan odamlar: <b>{s['total_users']}</b>\n"
        f"👪 Bot turgan guruhlar soni: <b>{s['total_groups']}</b>\n"
        f"🗓 So'nggi 7 kunda javob berilganlar: <b>{s['weekly_users']}</b>\n"
        f"📅 So'nggi 30 kunda javob berilganlar: <b>{s['monthly_users']}</b>"
    )


# ---------- Guruhga qo'shilish / chiqarilish ----------

@dp.my_chat_member()
async def on_bot_membership_change(event: ChatMemberUpdated):
    if event.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        return

    new_status = event.new_chat_member.status
    if new_status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
        await db.add_group(event.chat.id, event.chat.title or "Noma'lum guruh")
        logger.info(f"Guruhga qo'shildi: {event.chat.title!r} ({event.chat.id})")
    elif new_status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
        await db.deactivate_group(event.chat.id)
        logger.info(f"Guruhdan chiqarildi: {event.chat.title!r} ({event.chat.id})")


# ---------- Guruhdagi xabarlarga avtomatik javob ----------

@dp.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def on_group_message(message: Message):
    if not message.from_user or message.from_user.is_bot:
        return

    user_id = message.from_user.id

    if config.REPLY_ONCE_PER_USER and await db.has_replied(user_id):
        return

    try:
        await message.reply(AUTO_REPLY_TEXT, reply_markup=reply_keyboard())
        await db.log_reply(user_id, message.from_user.first_name or "", message.chat.id)
        logger.info(f"Javob yuborildi: {user_id} ({message.chat.title})")
    except Exception as e:
        logger.warning(f"Javob yuborib bo'lmadi ({user_id}): {e}")


# ---------- Admin panel (faqat ADMIN_ID uchun, shaxsiy chatda) ----------

@dp.message(Command("admin"), F.chat.type == ChatType.PRIVATE)
async def admin_panel(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
    await message.answer(await stats_text(), reply_markup=admin_refresh_keyboard())


@dp.callback_query(F.data == "refresh_stats")
async def refresh_stats(callback: CallbackQuery):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return
    try:
        await callback.message.edit_text(await stats_text(), reply_markup=admin_refresh_keyboard())
    except Exception:
        pass  # matn o'zgarmagan bo'lsa Telegram xato qaytaradi - bu muammo emas
    await callback.answer("Yangilandi")


@dp.message(Command("start"), F.chat.type == ChatType.PRIVATE)
async def start_cmd(message: Message):
    await message.answer("Salom! Bot ishlamoqda.")


# ---------- Ishga tushirish ----------

async def main():
    await db.init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
