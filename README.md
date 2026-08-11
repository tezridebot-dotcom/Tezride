# Guruh reklama-bot

Bot guruhga admin qilib qo'yiladi va guruhda yozgan har bir odamga (standart holatda — faqat bir marta)
avtomatik xabar bilan javob yozadi. Xabar ostida **"Habar berish"** tugmasi bo'ladi — u alohida
belgilangan shaxsning shaxsiy chatiga olib boradi. Bundan tashqari alohida **admin** statistikani
(`/admin`) ko'ra oladi.

## Fayllar

| Fayl | Vazifasi |
|---|---|
| `bot.py` | Botning asosiy logikasi |
| `config.py` | Muhit o'zgaruvchilarini o'qiydi |
| `messages.py` | Avtomatik javob matni va tugma yozuvi (shu yerdan tahrirlanadi) |
| `database.py` | SQLite bilan ishlash (statistika, guruhlar) |
| `requirements.txt` | Kerakli kutubxonalar |
| `Procfile` | Railway uchun ishga tushirish buyrug'i |

## 1. Bot yaratish

1. Telegram'da **@BotFather** ga yozing → `/newbot` → nom va username bering.
2. Sizga token beradi (masalan `123456:AAExample...`) — buni saqlab qo'ying.
3. Ishonch uchun (majburiy emas, chunki admin-bot barcha xabarlarni ko'radi):
   `/mybots` → botingiz → **Bot Settings → Group Privacy → Turn off**.

## 2. ID larni topish

- O'zingizning yoki boshqa odamning Telegram ID raqamini bilish uchun **@userinfobot** ga yozing.
- `ADMIN_ID` — statistika (`/admin`) ni ko'radigan shaxs.
- `CONTACT_ID` — "Habar berish" tugmasi orqali murojaat qabul qiladigan shaxs.
  Bular ikkita **har xil** odam bo'lishi mumkin.

> **Eslatma:** `tg://user?id=...` link ba'zi hollarda to'g'ridan-to'g'ri ochilmasligi mumkin
> (Telegramning cheklovi tufayli). Agar shunday bo'lsa, `CONTACT_ID` egasining public
> username'i bo'lsa, `.env` faylida `CONTACT_USERNAME=username` qatorini qo'shing — u holda
> tugma `https://t.me/username` orqali ishlaydi, bu 100% ishlaydi.

## 3. Mahalliy ishga tushirish (ixtiyoriy, tekshirish uchun)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env faylini oching va BOT_TOKEN, ADMIN_ID, CONTACT_ID qiymatlarini kiriting
python bot.py
```

## 4. GitHub'ga joylash

```bash
git init
git add .
git commit -m "Guruh reklama-bot"
git branch -M main
git remote add origin https://github.com/<username>/<repo-nomi>.git
git push -u origin main
```

`.env` fayli `.gitignore`da bor — token GitHub'ga tushib qolmaydi. Faqat `.env.example` yuklanadi.

## 5. Railway'da ishga tushirish

1. [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo** → shu repo'ni tanlang.
2. **Variables** bo'limiga quyidagilarni qo'shing:
   - `BOT_TOKEN`
   - `ADMIN_ID`
   - `CONTACT_ID`
   - `CONTACT_USERNAME` (agar kerak bo'lsa)
   - `REPLY_ONCE_PER_USER` (`true` yoki `false`)
3. Railway `Procfile`ni ko'rib, `worker` sifatida ishga tushiradi — bu bot uchun to'g'ri, chunki
   u web-server emas, doimiy ishlab turuvchi jarayon (polling). Public domain/port ochish shart emas.
4. **Statistikani saqlab qolish uchun (tavsiya etiladi):** Railway loyihangizga bitta **Volume**
   qo'shib, uni ilova papkasiga (masalan `/app/data`) ulang va `DB_PATH=/app/data/bot_data.db`
   qilib qo'ying. Aks holda har safar qayta deploy qilinganda statistika fayli o'chib, noldan
   boshlanadi (bot o'zi normal ishlayveradi, faqat eski statistika yo'qoladi).

## 6. Botni guruhga qo'shish

1. Botni kerakli guruh(lar)ga qo'shing.
2. Uni **admin** qiling (kamida "Send Messages" huquqi bo'lsa yetarli).
3. Shundan keyin guruhda kimdir yozganda, bot avtomatik javob yozadi.

## 7. Admin panel

Botga shaxsiy (lichka) xabarda `/admin` deb yozing — lekin faqat `ADMIN_ID` sifatida
ko'rsatilgan shaxsga javob beradi, boshqalarga hech narsa qaytarmaydi. Panelda:

- Jami javob berilgan odamlar soni
- Bot turgan (faol) guruhlar soni
- So'nggi 7 kunda javob berilganlar soni
- So'nggi 30 kunda javob berilganlar soni

"🔄 Yangilash" tugmasi orqali raqamlarni yangilash mumkin.

## Sozlash bo'yicha eslatmalar

- Avtomatik xabar matnini o'zgartirish uchun **faqat** `messages.py` faylini tahrirlang.
- Standart holatda bot har odamga **faqat bir marta** javob yozadi (`REPLY_ONCE_PER_USER=true`),
  aks holda bir kishi guruhda ko'p yozsa, bot har safar javob yozib spam bo'lib ketadi.
  Agar chindan ham har xabarga javob kerak bo'lsa, `.env`da `REPLY_ONCE_PER_USER=false` qiling.
