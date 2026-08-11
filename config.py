import os
from dotenv import load_dotenv

load_dotenv()

# Bot tokeni (@BotFather dan olinadi)
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Statistika/admin panelni ko'ra oladigan shaxsning Telegram ID raqami
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# "Habar berish" tugmasi bosilganda murojaatlar boradigan shaxsning Telegram ID raqami
# (ADMIN_ID dan alohida bo'lishi mumkin)
CONTACT_ID = int(os.getenv("CONTACT_ID", "0"))

# Ixtiyoriy: agar CONTACT shaxsning public username'i bo'lsa, shuni yozing.
# Bo'lsa, tugma https://t.me/username orqali ishlaydi (bu 100% ishonchli usul).
# Bo'lmasa, tg://user?id=... orqali ochishga harakat qilinadi (ba'zan ishlamasligi mumkin).
CONTACT_USERNAME = os.getenv("CONTACT_USERNAME", "").lstrip("@")

# True bo'lsa - bot har bir odamga FAQAT BIR MARTA javob yozadi (tavsiya etiladi).
# False bo'lsa - guruhda yozgan HAR BIR xabarga javob beradi (spam bo'lib ketishi mumkin).
REPLY_ONCE_PER_USER = os.getenv("REPLY_ONCE_PER_USER", "true").lower() == "true"

# Ma'lumotlar bazasi fayli
DB_PATH = os.getenv("DB_PATH", "bot_data.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN topilmadi. .env faylini yarating yoki Railway'da "
        "Environment Variables bo'limiga BOT_TOKEN qo'shing."
    )
