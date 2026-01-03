from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import logging
import asyncio

from config import BOT_TOKEN, ADMIN_IDS, CHANNEL_ID
import database
from states import RegistrationStates
import keyboards
from aiogram.dispatcher import FSMContext

# Logging sozlash
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Obunani tekshirish funksiyasi
async def check_user_sub(user_id):
    if not CHANNEL_ID:
        return True
    try:
        # CHANNEL_ID ni tozalash (@ yoki t.me/ dan)
        clean_cid = CHANNEL_ID.replace("https://t.me/", "").replace("http://t.me/", "").replace("t.me/", "").replace("@", "")
        member = await bot.get_chat_member(f"@{clean_cid}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# Middleware o'rniga oddiy tekshiruv (yoki handlerlarda)
async def is_subscribed(message: types.Message):
    if not await check_user_sub(message.from_user.id):
        clean_cid = CHANNEL_ID.replace("https://t.me/", "").replace("http://t.me/", "").replace("t.me/", "").replace("@", "")
        url = f"tg://resolve?domain={clean_cid}"
        await message.answer(
            "Klub a’zosi sifatida quyidagi sahifaga obuna bo‘lishingiz shart:",
            reply_markup=keyboards.get_sub_kb(url)
        )
        return False
    return True

# --- USER HANDLERS ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.answer("Xush kelibsiz, Admin!", reply_markup=keyboards.get_admin_main_kb())
        return

    await message.answer(
        "Assalomu alaykum!\nSiz ECOTECH Club’ga a’zo bo‘lish uchun rasmiy ro‘yxatdan o‘tish botidasiz.\nDavom etish uchun pastdagi tugmani bosing.",
        reply_markup=keyboards.get_start_kb()
    )

@dp.message_handler(lambda message: message.text == "🟢 Ro‘yxatdan o‘tish")
async def start_registration(message: types.Message):
    user = await database.get_user(message.from_user.id)
    if user:
        if user[12] == 'approved':
            await message.answer("Siz allaqachon a'zo bo'lgansiz!")
            return
        elif user[12] == 'pending':
            await message.answer("Sizning arizangiz ko'rib chiqilmoqda.")
            return

    await RegistrationStates.full_name.set()
    await message.answer(
        "To‘liq ism, familiya va otangizning ismini kiriting.\n(Masalan: Ibroximov Isroiljon Akmalovich)",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message_handler(state=RegistrationStates.full_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await RegistrationStates.next()
    await message.answer("Tug‘ilgan sanangizni kiriting.\n(Masalan: 15.08.2003)")

@dp.message_handler(state=RegistrationStates.birth_date)
async def process_birth(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await RegistrationStates.next()
    await message.answer("Jinsingizni tanlang:", reply_markup=keyboards.get_gender_kb())

@dp.message_handler(state=RegistrationStates.gender)
async def process_gender(message: types.Message, state: FSMContext):
    if message.text not in ["Erkak", "Ayol"]:
        await message.answer("Iltimos, tugmalardan birini tanlang.")
        return
    await state.update_data(gender=message.text)
    await RegistrationStates.next()
    await message.answer("Mutaxassisligingizni yozing.\n(Masalan: IT, Ekologiya, Muhandislik, Talaba va boshqalar)", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=RegistrationStates.specialty)
async def process_specialty(message: types.Message, state: FSMContext):
    await state.update_data(specialty=message.text)
    await RegistrationStates.next()
    await message.answer("Yashash manzilingizni kiriting.\n(Viloyat, tuman/shahar)")

@dp.message_handler(state=RegistrationStates.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await RegistrationStates.next()
    await message.answer("Telefon raqamingizni yuboring.", reply_markup=keyboards.get_phone_kb())

@dp.message_handler(state=RegistrationStates.phone, content_types=types.ContentTypes.CONTACT)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await RegistrationStates.next()
    await message.answer("Elektron pochta manzilingizni kiriting.\n(Masalan: example@gmail.com)", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=RegistrationStates.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await RegistrationStates.next()
    await message.answer("ECOTECH klubiga a’zo bo‘lishdan maqsadingizni yozing.")

@dp.message_handler(state=RegistrationStates.purpose)
async def process_purpose(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await RegistrationStates.next()
    await message.answer("Atrof-muhit, texnologiya yoki IT sohasida sizni eng ko‘p qiziqtiradigan mavzularni yozing.")

@dp.message_handler(state=RegistrationStates.interests)
async def process_interests(message: types.Message, state: FSMContext):
    await state.update_data(interests=message.text)
    await RegistrationStates.next()
    await message.answer("Avvalgi tajribangiz haqida yozing.\n(Tanlovlar, volontyorlik, loyihalar va boshqalar. Agar bo‘lmasa, “Yo‘q” deb yozing)")

@dp.message_handler(state=RegistrationStates.experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await RegistrationStates.next()
    await message.answer(
        "Klub faoliyatida qaysi shaklda ishtirok etmoqchisiz?\nShulardan birini tanlang va yozing ❗️",
        reply_markup=keyboards.get_participation_kb()
    )

@dp.message_handler(state=RegistrationStates.participation_type)
async def process_final(message: types.Message, state: FSMContext):
    await state.update_data(participation_type=message.text, user_id=message.from_user.id)
    data = await state.get_data()
    
    await database.add_user(data)
    await state.finish()
    
    await message.answer(
        "Rahmat! Sizning ma’lumotlaringiz adminga yuborildi.\nMa’lumotlar ko‘rib chiqilgach, sizga javob beriladi.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    # Adminga xabar yuborish
    admin_text = (
        f"🆕 Yangi a’zo arizasi:\n\n"
        f"F.I.O: {data['full_name']}\n"
        f"Tug‘ilgan sana: {data['birth_date']}\n"
        f"Jinsi: {data['gender']}\n"
        f"Mutaxassislik: {data['specialty']}\n"
        f"Manzil: {data['address']}\n"
        f"Telefon: {data['phone']}\n"
        f"Email: {data['email']}\n\n"
        f"Maqsad: {data['purpose']}\n"
        f"Qiziqishlar: {data['interests']}\n"
        f"Tajriba: {data['experience']}\n"
        f"Ishtirok shakli: {data['participation_type']}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, admin_text, reply_markup=keyboards.get_approval_kb(message.from_user.id))
        except Exception:
            pass

# --- ADMIN HANDLERS ---

@dp.callback_query_handler(lambda c: c.data.startswith('approve_'))
async def approve_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    await database.update_status(user_id, 'approved')
    await callback.answer("Ariza qabul qilindi!")
    await bot.send_message(user_id, "🎉 Tabriklaymiz!\nSiz ECOTECH klubiga qabul qilindingiz.\nSiz uchun profil yaratildi.")
    
    # Obuna bo'lishni so'rash
    clean_cid = CHANNEL_ID.replace("https://t.me/", "").replace("http://t.me/", "").replace("t.me/", "").replace("@", "")
    channel_url = f"tg://resolve?domain={clean_cid}"

    await bot.send_message(
        user_id, 
        "Klub a’zosi sifatida quyidagi sahifaga obuna bo‘lishingiz shart:", 
        reply_markup=keyboards.get_sub_kb(channel_url)
    )
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"Foydalanuvchi {user_id} qabul qilindi.")

@dp.callback_query_handler(lambda c: c.data.startswith('reject_'))
async def reject_user(callback: types.CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    await database.update_status(user_id, 'rejected')
    await callback.answer("Ariza rad etildi.")
    await bot.send_message(user_id, "Afsuski, sizning arizangiz rad etildi.")
    await callback.message.edit_reply_markup(reply_markup=None)

@dp.message_handler(lambda message: message.text == "👥 A’zolar" and message.from_user.id in ADMIN_IDS)
async def show_members(message: types.Message):
    members = await database.get_all_members()
    if not members:
        await message.answer("Hozircha a'zolar yo'q.")
        return
    text = "Klub a'zolari ro'yxati:\n\n"
    for i, (name, uid) in enumerate(members, 1):
        text += f"{i}. {name} (ID: {uid})\n"
    await message.answer(text)

@dp.message_handler(lambda message: message.text == "❌ A’zoni o‘chirish" and message.from_user.id in ADMIN_IDS)
async def delete_member_prompt(message: types.Message):
    await message.answer("O'chirmoqchi bo'lgan a'zoning Telegram ID sini yuboring:")

@dp.message_handler(lambda message: message.from_user.id in ADMIN_IDS and message.text.isdigit())
async def process_deletion(message: types.Message):
    uid = int(message.text)
    user = await database.get_user(uid)
    if user:
        await database.delete_user(uid)
        await message.answer(f"Foydalanuvchi {user[1]} (ID: {uid}) bazadan o'chirildi.")
    else:
        await message.answer("Bunday ID dagi foydalanuvchi topilmadi.")

@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery):
    if await check_user_sub(callback.from_user.id):
        await callback.answer("Rahmat, obuna tasdiqlandi!", show_alert=True)
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, "Siz barcha shartlarni bajardingiz! Botdan to'liq foydalanishingiz mumkin.")
    else:
        await callback.answer("Hali obuna bo'lmagansiz!", show_alert=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(database.init_db())
    executor.start_polling(dp, skip_updates=True)
