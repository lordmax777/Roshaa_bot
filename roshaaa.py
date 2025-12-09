import os
import asyncio
import logging
from typing import Dict, Any, Optional

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = os.getenv("API_TOKEN")   # BotFather dan token ENV orqali
HR_CHAT_ID = int(os.getenv("HR_CHAT_ID", "-1003484007737"))  # default qo'yib qo'ydik, lekin ENVdan ham oladi

logging.basicConfig(level=logging.INFO)

bot = Bot(
    API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
router = Router()
dp.include_router(router)

# user_data[user_id] = foydalanuvchi anketa va jarayon holati
user_data: Dict[int, Dict[str, Any]] = {}

# ================== YORDAMCHI FUNKSIYALAR ==================
def tr(uid: int, uz: str, ru: str) -> str:
    """Til bo‘yicha tarjima."""
    lang = user_data.get(uid, {}).get("lang", "uz")
    return uz if lang == "uz" else ru


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📌 Kompaniya haqida")
                if lang == "uz"
                else KeyboardButton(text="📌 О компании")
            ],
            [
                KeyboardButton(text="📝 Ro‘yxatdan o‘tish")
                if lang == "uz"
                else KeyboardButton(text="📝 Регистрация")
            ],
        ],
        resize_keyboard=True,
    )


def department_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = [
            "Sotuv bo‘limi",
            "Ombor bo‘limi",
            "Kassa",
        ]
    else:
        labels = [
            "Отдел продаж",
            "Склад",
            "Касса",
        ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
                KeyboardButton(text=labels[2]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def nationality_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = ["O‘zbek", "Rus", "Tojik", "Boshqa"]
    else:
        labels = ["Узбек", "Русский", "Таджик", "Другое"]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
            ],
            [
                KeyboardButton(text=labels[2]),
                KeyboardButton(text=labels[3]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def education_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = ["Oliy", "Oliy / tugallanmagan", "O‘rta maxsus", "O‘rta"]
    else:
        labels = ["Высшее", "Незаконченное высшее", "Среднее специальное", "Среднее"]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
            ],
            [
                KeyboardButton(text=labels[2]),
                KeyboardButton(text=labels[3]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def marital_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = [
            "Uylangan / turmush qurgan",
            "Uylanmagan / turmush qurmagan",
            "Ajrashgan",
        ]
    else:
        labels = [
            "Женат / Замужем",
            "Холост / Не замужем",
            "В разводе",
        ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
            ],
            [
                KeyboardButton(text=labels[2]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def habits_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = [
            "Chekish",
            "Ichish",
            "Chekish va ichish",
            "Zararli odatlar yo‘q",
        ]
    else:
        labels = [
            "Курю",
            "Пью",
            "Курю и пью",
            "Вредных привычек нет",
        ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
            ],
            [
                KeyboardButton(text=labels[2]),
                KeyboardButton(text=labels[3]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def percent_keyboard(lang: str) -> ReplyKeyboardMarkup:
    labels = ["0%", "25%", "50%", "75%", "100%"]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
                KeyboardButton(text=labels[2]),
            ],
            [
                KeyboardButton(text=labels[3]),
                KeyboardButton(text=labels[4]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def source_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = [
            "Telegram reklama",
            "Instagram",
            "Tanishlar",
            "Ish e’lon sayti",
            "Boshqa",
        ]
    else:
        labels = [
            "Реклама в Telegram",
            "Instagram",
            "Знакомые",
            "Сайт вакансий",
            "Другое",
        ]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
            ],
            [
                KeyboardButton(text=labels[2]),
                KeyboardButton(text=labels[3]),
            ],
            [
                KeyboardButton(text=labels[4]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def shift_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = ["Ertalab smena", "Kechqurun smena", "Aralash smena"]
    else:
        labels = ["Утренняя смена", "Вечерняя смена", "Смешанная смена"]

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=labels[0]),
                KeyboardButton(text=labels[1]),
                KeyboardButton(text=labels[2]),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def yesno_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        labels = ["Ha", "Yo‘q"]
    else:
        labels = ["Да", "Нет"]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=l) for l in labels]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 O‘zbek"),
                KeyboardButton(text="🇷🇺 Русский"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def ask_step_question(uid: int, message: Message):
    """Hozirgi step bo‘yicha foydalanuvchidan keyingi savolni so‘rash."""
    data = user_data[uid]
    lang = data.get("lang", "uz")
    step = data.get("step")

    # Har bir step uchun savol va klaviatura:
    if step == "name":
        await message.answer(
            tr(
                uid,
                "Ro‘yxatdan o‘tishni boshlaymiz.\n\nIltimos, <b>Ism Familyangizni</b> kiriting:",
                "Начнем регистрацию.\n\nПожалуйста, введите ваше <b>Имя и Фамилию</b>:",
            ),
            reply_markup=ReplyKeyboardRemove(),
        )

    elif step == "birth":
        await message.answer(
            tr(
                uid,
                "Tug‘ilgan sanangizni kiriting (masalan, 01.01.1990):",
                "Введите вашу дату рождения (например, 01.01.1990):",
            )
        )

    elif step == "phone":
        phone_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text=tr(uid, "📲 Telefon raqamni ulashish", "📲 Поделиться номером"),
                        request_contact=True,
                    )
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await message.answer(
            tr(
                uid,
                "Telefon raqamingizni yuborish uchun tugmani bosing yoki o‘zingiz yozib yuboring:",
                "Нажмите кнопку, чтобы отправить номер телефона, или введите его вручную:",
            ),
            reply_markup=phone_kb,
        )

    elif step == "department":
        await message.answer(
            tr(
                uid,
                "Qaysi bo‘limga ishga kirmoqchisiz?",
                "В какой отдел вы хотите устроиться?",
            ),
            reply_markup=department_keyboard(lang),
        )

    elif step == "address":
        await message.answer(
            tr(
                uid,
                "Yashash manzilingizni yozing (ko‘cha, uy, tuman, shahar):",
                "Напишите ваш адрес проживания (улица, дом, район, город):",
            ),
            reply_markup=ReplyKeyboardRemove(),
        )

    elif step == "nationality":
        await message.answer(
            tr(uid, "Millatingizni tanlang:", "Выберите вашу национальность:"),
            reply_markup=nationality_keyboard(lang),
        )

    elif step == "education":
        await message.answer(
            tr(uid, "Ma’lumotingizni tanlang:", "Выберите ваше образование:"),
            reply_markup=education_keyboard(lang),
        )

    elif step == "marital":
        await message.answer(
            tr(uid, "Oylaviy holatingizni tanlang:", "Выберите ваше семейное положение:"),
            reply_markup=marital_keyboard(lang),
        )

    elif step == "habits":
        await message.answer(
            tr(uid, "Zararli odatlaringiz:", "Вредные привычки:"),
            reply_markup=habits_keyboard(lang),
        )

    elif step == "lang_ru":
        await message.answer(
            tr(
                uid,
                "Rus tilini bilish darajangizni tanlang:",
                "Выберите уровень владения русским языком:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "lang_en":
        await message.answer(
            tr(
                uid,
                "Ingliz tilini bilish darajangizni tanlang:",
                "Выберите уровень владения английским языком:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "lang_cn":
        await message.answer(
            tr(
                uid,
                "Xitoy tilini bilish darajangizni tanlang:",
                "Выберите уровень владения китайским языком:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "skill_word":
        await message.answer(
            tr(
                uid,
                "Word dasturini bilish darajangizni tanlang:",
                "Выберите уровень владения Word:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "skill_excel":
        await message.answer(
            tr(
                uid,
                "Excel dasturini bilish darajangizni tanlang:",
                "Выберите уровень владения Excel:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "skill_onec":
        await message.answer(
            tr(
                uid,
                "1C dasturini bilish darajangizni tanlang:",
                "Выберите уровень владения 1C:",
            ),
            reply_markup=percent_keyboard(lang),
        )

    elif step == "source_info":
        await message.answer(
            tr(
                uid,
                "Kompaniyamiz haqida qayerdan ma’lumot oldingiz?",
                "Откуда вы узнали о нашей компании?",
            ),
            reply_markup=source_keyboard(lang),
        )

    elif step == "prev_job":
        await message.answer(
            tr(
                uid,
                "Avvalgi ish joyingiz? (kompaniya va lavozim):",
                "Ваше предыдущее место работы? (компания и должность):",
            ),
            reply_markup=ReplyKeyboardRemove(),
        )

    elif step == "salary":
        await message.answer(
            tr(
                uid,
                "Hohlayotgan ish haqqingizni kiriting:",
                "Введите желаемую заработную плату:",
            )
        )

    elif step == "shift":
        await message.answer(
            tr(
                uid,
                "Qaysi smenada ishlay olasiz?",
                "В какую смену вы можете работать?",
            ),
            reply_markup=shift_keyboard(lang),
        )

    elif step == "ref_check":
        await message.answer(
            tr(
                uid,
                "Eski ish joyingizdan va yashash joyingizdan surishtirishga qarshiligingiz yo‘qmi?",
                "Вы не против, если мы наведём справки с вашего прошлого места работы и места жительства?",
            ),
            reply_markup=yesno_keyboard(lang),
        )

    elif step == "photo":
        await message.answer(
            tr(
                uid,
                "Iltimos, fotosuratingizni yuboring:",
                "Пожалуйста, отправьте ваше фото:",
            ),
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=tr(uid, "Bekor qilish", "Отменить"))]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )


# ================== /start (PAUZA / DAVOM ETTIRISH) ==================

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    uid = message.from_user.id
    data = user_data.get(uid)

    # Agar oldin boshlangan, lekin tugallanmagan ariza bo‘lsa:
    if data and data.get("step") not in (None, "completed", "resume_choice"):
        data["saved_step"] = data["step"]
        data["step"] = "resume_choice"

        lang = data.get("lang", "uz")
        text = (
            "Siz ilgari boshlangan, lekin tugallanmagan arizaga egasiz.\n"
            "Uni davom ettirmoqchimisiz?"
            if lang == "uz"
            else "У вас есть незавершённая заявка.\nХотите продолжить заполнение?"
        )
        kb = yesno_keyboard(lang)
        await message.answer(text, reply_markup=kb)
        return

    # Aks holda – til tanlashdan oldin chiroyli salomlashamiz
    first_name = message.from_user.first_name or ""
    greeting_text = (
        f"🇺🇿Assalomu alaykum {first_name}.\n"
        f"Roshaa Market botiga xush kelibsiz!\n" 
        f"Pastdan tilni tanlang:\n\n"
        f"🇷🇺Здравствуйте {first_name}.\n"
        f"Добро пожаловать в бот Roshaa Market!\n"
        f"Выберите язык внизу:"
        
    )

    await message.answer(greeting_text, reply_markup=language_keyboard())



@router.message(F.text.in_(["🇺🇿 O‘zbek", "🇷🇺 Русский"]))
async def choose_language(message: Message):
    uid = message.from_user.id

    if uid in user_data and user_data[uid].get("step") not in (None, "completed"):
        # Agar qandaydir eski holat qolgan bo‘lsa – tozalaymiz (foydalanuvchi yangidan boshlashni xohlagan bo‘ladi)
        user_data.pop(uid, None)

    if message.text.startswith("🇺🇿"):
        lang = "uz"
    else:
        lang = "ru"

    user_data[uid] = {
        "lang": lang,
        "username": message.from_user.username,
        "step": None,
    }

    text = (
        "Assalomu alaykum! Marhamat, bo‘limni tanlang 👇"
        if lang == "uz"
        else "Здравствуйте! Выберите раздел 👇"
    )

    await message.answer(text, reply_markup=main_menu_keyboard(lang))


# ================== KOMPANIYA HAQIDA ==================

@router.message(F.text.in_(["📌 Kompaniya haqida", "📌 О компании"]))
async def about_company(message: Message):
    uid = message.from_user.id
    user_data.setdefault(uid, {})
    text = tr(
        uid,
        uz=(
            "📌 <b>Kompaniya haqida qisqacha ma’lumot</b>\n\n"
            "📱 Telegram kanal: @shukurxon800_zaa\n"
            "📞 Call-markaz: +998-90-634-44-44"
        ),
        ru=(
            "📌 <b>Краткая информация о компании</b>\n\n"
            "📱 Telegram-канал: @shukurxon800_zaa\n"
            "📞 Call-центр: +998-90-634-44-44"
        ),
    )
    await message.answer(text)


# ================== RO‘YXATDAN O‘TISH BOSHLANISHI ==================

@router.message(F.text.in_(["📝 Ro‘yxatdan o‘tish", "📝 Регистрация"]))
async def register_start(message: Message):
    uid = message.from_user.id
    user_data.setdefault(uid, {})
    if "lang" not in user_data[uid]:
        user_data[uid]["lang"] = "uz"
    user_data[uid]["username"] = message.from_user.username
    user_data[uid]["step"] = "name"
    await ask_step_question(uid, message)


# ================== ASOSIY FORM BOSQICHLARI (MESSAGE HANDLER) ==================

@router.message()
async def form_steps(message: Message):
    uid = message.from_user.id
    if uid not in user_data or "step" not in user_data[uid]:
        return

    data = user_data[uid]
    step = data["step"]
    lang = data.get("lang", "uz")
    text = message.text or ""

    # Davom ettirish savoliga javob
    if step == "resume_choice":
        if lang == "uz":
            yes, no = "Ha", "Yo‘q"
        else:
            yes, no = "Да", "Нет"

        if text == yes:
            # avvalgi stepga qaytamiz
            saved_step = data.get("saved_step")
            if saved_step:
                data["step"] = saved_step
                data.pop("saved_step", None)
                await ask_step_question(uid, message)
            else:
                # xavfsizlik uchun yangidan
                data["step"] = None
                await message.answer(
                    tr(
                        uid,
                        "Ro‘yxatdan o‘tishni yangidan boshlaymiz.",
                        "Начнём регистрацию заново.",
                    ),
                    reply_markup=language_keyboard(),
                )
            return
        elif text == no:
            # eski ma'lumotlarni o‘chirib, boshidan
            user_data.pop(uid, None)
            await message.answer(
                tr(
                    uid,
                    "Yangi ariza boshlash uchun tilni tanlang:",
                    "Чтобы начать новую заявку, выберите язык:",
                ),
                reply_markup=language_keyboard(),
            )
            return
        else:
            await message.answer(
                tr(
                    uid,
                    "Iltimos, pastdagi tugmalardan birini tanlang: Ha / Yo‘q",
                    "Пожалуйста, выберите один из вариантов: Да / Нет",
                )
            )
            return

    # 1) F.I.Sh
    if step == "name":
        data["name"] = text
        data["step"] = "birth"
        await ask_step_question(uid, message)
        return

    # 2) Tug‘ilgan sana
    if step == "birth":
        data["birth"] = text
        data["step"] = "phone"
        await ask_step_question(uid, message)
        return

    # 3) Telefon – contact yoki text
    if step == "phone":
        if message.contact:
            data["phone"] = message.contact.phone_number
        else:
            data["phone"] = text
        data["step"] = "department"
        await ask_step_question(uid, message)
        return

    # 4) Bo‘lim
    if step == "department":
        data["department"] = text
        data["step"] = "address"
        await ask_step_question(uid, message)
        return

    # 5) Manzil
    if step == "address":
        data["address_text"] = text
        data["step"] = "nationality"
        await ask_step_question(uid, message)
        return

    # 6) Millat
    if step == "nationality":
        data["nationality"] = text
        data["step"] = "education"
        await ask_step_question(uid, message)
        return

    # 7) Ma’lumoti
    if step == "education":
        data["education"] = text
        data["step"] = "marital"
        await ask_step_question(uid, message)
        return

    # 8) Oylaviy holat
    if step == "marital":
        data["marital"] = text
        data["step"] = "habits"
        await ask_step_question(uid, message)
        return

    # 9) Zararli odatlar
    if step == "habits":
        data["habits"] = text
        data["step"] = "lang_ru"
        await ask_step_question(uid, message)
        return

    # 10) Rus tili
    if step == "lang_ru":
        data["ru_level"] = text.replace("%", "").strip()
        data["step"] = "lang_en"
        await ask_step_question(uid, message)
        return

    # 11) Ingliz tili
    if step == "lang_en":
        data["en_level"] = text.replace("%", "").strip()
        data["step"] = "lang_cn"
        await ask_step_question(uid, message)
        return

    # 12) Xitoy tili
    if step == "lang_cn":
        data["cn_level"] = text.replace("%", "").strip()
        data["step"] = "skill_word"
        await ask_step_question(uid, message)
        return

    # 13) Word
    if step == "skill_word":
        data["word_level"] = text.replace("%", "").strip()
        data["step"] = "skill_excel"
        await ask_step_question(uid, message)
        return

    # 14) Excel
    if step == "skill_excel":
        data["excel_level"] = text.replace("%", "").strip()
        data["step"] = "skill_onec"
        await ask_step_question(uid, message)
        return

    # 15) 1C
    if step == "skill_onec":
        data["onec_level"] = text.replace("%", "").strip()
        data["step"] = "source_info"
        await ask_step_question(uid, message)
        return

    # 16) Kompaniya haqida qayerdan eshitgan
    if step == "source_info":
        data["source_info"] = text
        data["step"] = "prev_job"
        await ask_step_question(uid, message)
        return

    # 17) Avvalgi ish joyi
    if step == "prev_job":
        data["prev_job"] = text
        data["step"] = "salary"
        await ask_step_question(uid, message)
        return

    # 18) Ish haqi
    if step == "salary":
        data["salary"] = text
        data["step"] = "shift"
        await ask_step_question(uid, message)
        return

    # 19) Smena
    if step == "shift":
        data["shift"] = text
        data["step"] = "ref_check"
        await ask_step_question(uid, message)
        return

    # 20) Surishtirishga ruxsat
    if step == "ref_check":
        if lang == "uz":
            yes, no = "Ha", "Yo‘q"
        else:
            yes, no = "Да", "Нет"

        data["ref_check"] = "yes" if text == yes else "no"
        data["step"] = "photo"
        await ask_step_question(uid, message)
        return

    # 21-22) Foto
    if step == "photo":
        if not message.photo:
            await message.answer(
                tr(
                    uid,
                    "Iltimos, fotosuratingizni yuboring.",
                    "Пожалуйста, отправьте ваше фото.",
                )
            )
            return

        data["photo"] = message.photo[-1].file_id
        data["step"] = "confirm"
        await send_preview(uid, message)
        return


# ================== PREVIEW (TEKSHIRISH) ==================

async def send_preview(uid: int, message: Message):
    d = user_data[uid]

    def percent(v: Optional[str]) -> str:
        return (v or "0") + "%"

    addr = d.get("address_text") or tr(uid, "Ko‘rsatilmagan", "Не указано")

    username = d.get("username")
    if username:
        username_display = f"@{username}"
    else:
        username_display = tr(uid, "Ko‘rsatilmagan", "Не указано")

    ref_text = tr(
        uid,
        uz="Ruxsat beraman" if d.get("ref_check") == "yes" else "Ruxsat bermayman",
        ru="Разрешаю" if d.get("ref_check") == "yes" else "Не разрешаю",
    )

    text = tr(
        uid,
        uz="Iltimos, kiritgan ma’lumotlaringizni yana bir bor tekshirib chiqing:\n\n",
        ru="Пожалуйста, внимательно проверьте введённые данные:\n\n",
    )

    text += (
        f"👤 <b>F.I.Sh:</b> {d.get('name','')}\n"
        f"👤 <b>Telegram username:</b> {username_display}\n"
        f"🎂 <b>Tug‘ilgan sana:</b> {d.get('birth','')}\n"
        f"📞 <b>Telefon:</b> {d.get('phone','')}\n"
        f"🏢 <b>Bo‘lim:</b> {d.get('department','')}\n"
        f"📍 <b>Yashash manzil:</b> {addr}\n"
        f"🌐 <b>Millat:</b> {d.get('nationality','')}\n"
        f"🎓 <b>Ma’lumoti:</b> {d.get('education','')}\n"
        f"💍 <b>Oylaviy holat:</b> {d.get('marital','')}\n"
        f"🚬 <b>Zararli odatlar:</b> {d.get('habits','')}\n\n"
        f"🗣 <b>Tillar:</b>\n"
        f"▪️ Rus tili: {percent(d.get('ru_level'))}\n"
        f"▪️ Ingliz tili: {percent(d.get('en_level'))}\n"
        f"▪️ Xitoy tili: {percent(d.get('cn_level'))}\n\n"
        f"💻 <b>Kompyuter ko‘nikmalari:</b>\n"
        f"▪️ Word: {percent(d.get('word_level'))}\n"
        f"▪️ Excel: {percent(d.get('excel_level'))}\n"
        f"▪️ 1C: {percent(d.get('onec_level'))}\n\n"
        f"ℹ️ <b>Kompaniya haqida qayerdan eshitdingiz:</b> {d.get('source_info','')}\n"
        f"💼 <b>Avvalgi ish joyingiz:</b> {d.get('prev_job','')}\n"
        f"💰 <b>Hohlayotgan ish haqi:</b> {d.get('salary','')}\n"
        f"🕒 <b>Smena:</b> {d.get('shift','')}\n"
        f"📋 <b>Surishtirishga ruxsat:</b> {ref_text}\n"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=tr(uid, "✅ Tasdiqlash", "✅ Подтвердить"),
                    callback_data="confirm",
                )
            ],
            [
                InlineKeyboardButton(
                    text=tr(uid, "❌ Bekor qilish", "❌ Отменить"),
                    callback_data="cancel",
                )
            ],
        ]
    )

    await message.answer_photo(
        photo=d["photo"],
        caption=text,
        reply_markup=kb,
    )


# ================== TASDIQLASH – KANALGA YUBORISH + SMS-STYLE XABAR ==================

@router.callback_query(F.data == "confirm")
async def final_confirm(callback: CallbackQuery):
    uid = callback.from_user.id
    d = user_data.get(uid)
    if not d or "photo" not in d:
        await callback.answer("Xatolik. Ma'lumot topilmadi.", show_alert=True)
        return

    lang = d.get("lang", "uz")

    def percent(v: Optional[str]) -> str:
        return (v or "0") + "%"

    addr = d.get("address_text") or tr(uid, "Ko‘rsatilmagan", "Не указано")

    ref_text_uz = "Ruxsat beraman" if d.get("ref_check") == "yes" else "Ruxsat bermayman"
    ref_text_ru = "Разрешаю" if d.get("ref_check") == "yes" else "Не разрешаю"

    username = d.get("username")
    if username:
        username_display_uz = f"@{username}"
        username_display_ru = f"@{username}"
    else:
        username_display_uz = "Ko‘rsatilmagan"
        username_display_ru = "Не указано"

    if lang == "uz":
        text_hr = f"""
📨 <b>Yangi ishga qabul arizasi</b>

👤 <b>F.I.Sh:</b> {d.get('name','')}
👤 <b>Telegram username:</b> {username_display_uz}
🎂 <b>Tug‘ilgan sana:</b> {d.get('birth','')}
📞 <b>Telefon:</b> {d.get('phone','')}
🏢 <b>Talab qilayotgan bo‘lim:</b> {d.get('department','')}
📍 <b>Yashash manzili:</b> {addr}
🌐 <b>Millati:</b> {d.get('nationality','')}
🎓 <b>Ma’lumoti:</b> {d.get('education','')}
💍 <b>Oylaviy holati:</b> {d.get('marital','')}
🚬 <b>Zararli odatlari:</b> {d.get('habits','')}

🗣 <b>Tillar:</b>
▪️ Rus tili: {percent(d.get('ru_level'))}
▪️ Ingliz tili: {percent(d.get('en_level'))}
▪️ Xitoy tili: {percent(d.get('cn_level'))}

💻 <b>Kompyuter ko‘nikmalari:</b>
▪️ Word: {percent(d.get('word_level'))}
▪️ Excel: {percent(d.get('excel_level'))}
▪️ 1C: {percent(d.get('onec_level'))}

ℹ️ <b>Kompaniya haqida qayerdan eshitgan:</b> {d.get('source_info','')}
💼 <b>Avvalgi ish joyi:</b> {d.get('prev_job','')}
💰 <b>Hohlayotgan ish haqi:</b> {d.get('salary','')}
🕒 <b>Smena:</b> {d.get('shift','')}

📋 <b>Surishtirishga munosabati:</b> {ref_text_uz}

🆔 <b>Telegram ID:</b> <code>{uid}</code>
"""
        sms_text = (
            "✅ Arizangiz muvaffaqiyatli qabul qilindi!\n"
            "HR bo‘limi siz bilan 3 ish kuni ichida bog‘lanadi.\n"
            "Rahmat!"
        )
    else:
        text_hr = f"""
📨 <b>Новая заявка на трудоустройство</b>

👤 <b>Ф.И.О.:</b> {d.get('name','')}
👤 <b>Telegram username:</b> {username_display_ru}
🎂 <b>Дата рождения:</b> {d.get('birth','')}
📞 <b>Телефон:</b> {d.get('phone','')}
🏢 <b>Желаемый отдел:</b> {d.get('department','')}
📍 <b>Адрес проживания:</b> {addr}
🌐 <b>Национальность:</b> {d.get('nationality','')}
🎓 <b>Образование:</b> {d.get('education','')}
💍 <b>Семейное положение:</b> {d.get('marital','')}
🚬 <b>Вредные привычки:</b> {d.get('habits','')}

🗣 <b>Языки:</b>
▪️ Русский язык: {percent(d.get('ru_level'))}
▪️ Английский язык: {percent(d.get('en_level'))}
▪️ Китайский язык: {percent(d.get('cn_level'))}

💻 <b>Компьютерные навыки:</b>
▪️ Word: {percent(d.get('word_level'))}
▪️ Excel: {percent(d.get('excel_level'))}
▪️ 1C: {percent(d.get('onec_level'))}

ℹ️ <b>Источник информации о компании:</b> {d.get('source_info','')}
💼 <b>Предыдущее место работы:</b> {d.get('prev_job','')}
💰 <b>Желаемая зарплата:</b> {d.get('salary','')}
🕒 <b>Смена:</b> {d.get('shift','')}

📋 <b>Отношение к проверке рекомендаций:</b> {ref_text_ru}

🆔 <b>Telegram ID:</b> <code>{uid}</code>
"""
        sms_text = (
            "✅ Ваша заявка успешно принята!\n"
            "Наш HR-отдел свяжется с вами в течение 3 рабочих дней.\n"
            "Спасибо!"
        )

    # 1) HR kanal/guruhga yuboramiz
    await bot.send_photo(
        chat_id=HR_CHAT_ID,
        photo=d["photo"],
        caption=text_hr,
    )

    # 2) Preview xabarini o‘zgartiramiz
    done_text = tr(
        uid,
        "Arizangiz yuborildi ✅",
        "Ваша заявка отправлена ✅",
    )

    if callback.message.photo:
        await callback.message.edit_caption(done_text)
    else:
        await callback.message.edit_text(done_text)

    # 3) Nomzodga alohida "SMS-style" xabar
    await bot.send_message(chat_id=uid, text=sms_text)

    # 4) Ma'lumotlarni tozalaymiz
    user_data.pop(uid, None)


@router.callback_query(F.data == "cancel")
async def final_cancel(callback: CallbackQuery):
    uid = callback.from_user.id
    user_data.pop(uid, None)

    cancel_text = tr(
        uid,
        "Ariza bekor qilindi. Agar xohlasangiz, qayta /start bosib yangidan boshlashingiz mumkin.",
        "Заявка отменена. Если хотите, можете начать заново, отправив /start.",
    )

    if callback.message.photo:
        await callback.message.edit_caption(cancel_text)
    else:
        await callback.message.edit_text(cancel_text)


# ================== MAIN ==================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
