import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram import Router

# 🛡️ Токен и ID чата для уведомлений
BOT_TOKEN = "8035252263:AAE8h_GHbciC1aquIGAKgmhwesyNL86mrQk"
ADMIN_CHAT_ID = -1002693643570  # 🛑 Вставь сюда ID своей группы/чата

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()


# 💬 Сообщение при /start
TEXT = """
<b>5 СПОСОБОВ ЗАРАБОТАТЬ НА TELEGRAM-БОТАХ И КРИПТЕ</b>

1. <b>СОЗДАНИЕ БОТОВ НА ЗАКАЗ</b>
Востребованы боты-магазины, подписки, автопродажа товаров
Цена: от $300 до $1000
Можно брать заказы на фрилансе или запускать свои проекты

2. <b>ПРОДАЖА ГОТОВЫХ ШАБЛОНОВ</b>
Один раз разработал — можешь продавать сколько угодно
Средняя цена: $100–300
Пример: бот-магазин, бот с подпиской, крипто-бот

3. <b>ЗАПУСК СИГНАЛЬНОГО БОТА ПО КРИПТЕ</b>
Торговля на Binance, BingX, OKX — по сигналам
Люди платят за подписку ($30–100/мес)
С 50 подписчиков = стабильный доход

4. <b>СОЗДАНИЕ И ПРОДАЖА КУРСА</b>
Делишься опытом → записываешь мини-курс → запускаешь
Потенциал: 100 учеников по $99 = $9900
Курс можно автоматизировать через Telegram-бота

5. <b>АВТОМАТИЗИРОВАННАЯ ТОРГОВЛЯ КРИПТОЙ</b>
Сделал торгового бота → подключил API биржи → зарабатываешь
Подключаешь сигналы TradingView
Полностью автоматическая стратегия

Хочешь освоить Telegram-ботов и начать зарабатывать?
📲 Подписывайся на канал: https://t.me/getrade26

Жди старт курса:
@Fiodarjd1
@Vaitekaitis
"""

# Состояния
class CourseState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

# Хендлер /start
@router.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📲 Подписаться на канал", url="https://t.me/getrade26")]
        ]
    )
    await message.answer(TEXT, reply_markup=keyboard)

# Хендлер "Курс"
@router.message(F.text.lower() == "курс")
async def ask_name(message: types.Message, state: FSMContext):
    await state.set_state(CourseState.waiting_for_name)
    await message.answer("Как тебя зовут? 🙂", reply_markup=ReplyKeyboardRemove())

# Хендлер имени
@router.message(CourseState.waiting_for_name)
async def ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(CourseState.waiting_for_phone)
    await message.answer("Отправь, пожалуйста, свой номер телефона:", reply_markup=keyboard)

# Хендлер телефона
@router.message(CourseState.waiting_for_phone, F.contact)
async def finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    phone = message.contact.phone_number
    username = message.from_user.username or "Без ника"

    # Отправка в беседу
    msg = (
        f"📥 <b>Новая заявка на курс</b>\n\n"
        f"<b>Имя:</b> {name}\n"
        f"<b>Телефон:</b> {phone}\n"
        f"<b>Никнейм:</b> @{username}\n"
        f"<b>ID:</b> <code>{message.from_user.id}</code>"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

    # Подтверждение пользователю
    await message.answer("Спасибо! ✅ Мы скоро с тобой свяжемся.", reply_markup=ReplyKeyboardRemove())
    await state.clear()

dp.include_router(router)

async def main():
    # Удаляем webhook, если он был активен ранее
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем polling
    print("✅ Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
