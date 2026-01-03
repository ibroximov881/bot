from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import INSTAGRAM_LINK

def get_start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🟢 Ro‘yxatdan o‘tish")]],
        resize_keyboard=True
    )

def get_gender_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("Erkak"), KeyboardButton("Ayol")]
        ],
        resize_keyboard=True
    )

def get_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("📞 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

def get_participation_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("1️⃣ Doimiy aʼzo sifatida qatnashaman")],
            [KeyboardButton("2️⃣ Loyihada volontyor bo‘laman")],
            [KeyboardButton("3️⃣ Axborot texnologiyalari bo‘yicha ko‘mak beraman")],
            [KeyboardButton("4️⃣ Klubga homiylik qilaman")],
            [KeyboardButton("5️⃣ Boshqa")]
        ],
        resize_keyboard=True
    )

def get_admin_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("👥 A’zolar"), KeyboardButton("❌ A’zoni o‘chirish")]
        ],
        resize_keyboard=True
    )

def get_approval_kb(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("✅ Qabul qilish", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}")
        ]
    ])

def get_sub_kb(channel_url):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📢 Telegram kanal", url=channel_url)],
        [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")]
    ])
