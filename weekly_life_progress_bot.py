import nest_asyncio
nest_asyncio.apply()
import asyncio
import datetime
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Конфигурация ===
TOKEN = "7682758333:AAFYDUrGbux1B4NkhVAMl9eCHqMWeZfrYAo"  # Вставь сюда свой токен
CHAT_ID = "851557417"  # ID твоего чата
BIRTH_DATE = datetime.date(2006, 8, 9)  # Дата рождения
LIFE_EXPECTANCY_YEARS = 80  # До какого возраста считаем

# === Функция расчета недель жизни ===
def calculate_weeks():
    today = datetime.date.today()
    total_weeks = LIFE_EXPECTANCY_YEARS * 52  # Всего недель в жизни
    lived_weeks = (today - BIRTH_DATE).days // 7  # Прожито недель
    remaining_weeks = total_weeks - lived_weeks  # Осталось недель
    percent_lived = round((lived_weeks / total_weeks) * 100, 2)
    percent_remaining = round((remaining_weeks / total_weeks) * 100, 2)
    
    return lived_weeks, remaining_weeks, percent_lived, percent_remaining

# === Функция обработки команды /status ===
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lived_weeks, remaining_weeks, percent_lived, percent_remaining = calculate_weeks()
    message = (f"📅 **Текущая неделя:** {lived_weeks}\n"
               f"⏳ **Осталось:** {remaining_weeks} недель\n"
               f"📊 **Прожито:** {percent_lived}%\n"
               f"🔄 **Осталось:** {percent_remaining}%")
    await update.message.reply_text(message, parse_mode='Markdown')

# === Функция для еженедельных сообщений ===
async def send_weekly_message():
    bot = Bot(token=TOKEN)
    while True:
        now = datetime.datetime.now()
        next_monday = now + datetime.timedelta(days=(7 - now.weekday()))
        next_monday = next_monday.replace(hour=9, minute=0, second=0)
        time_to_sleep = (next_monday - now).total_seconds()
        
        await asyncio.sleep(time_to_sleep)  # Ждём до следующего понедельника
        lived_weeks, remaining_weeks, percent_lived, percent_remaining = calculate_weeks()
        message = (f"📅 **Текущая неделя:** {lived_weeks}\n"
                   f"⏳ **Осталось:** {remaining_weeks} недель\n"
                   f"📊 **Прожито:** {percent_lived}%\n"
                   f"🔄 **Осталось:** {percent_remaining}%")
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

# === Основной запуск бота ===
async def main():
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчик команды /status
    app.add_handler(CommandHandler("status", status))
    
    # Запускаем фоновый процесс для еженедельного сообщения
    asyncio.create_task(send_weekly_message())

    print("✅ Бот запущен!")
    await app.run_polling()

# === Запуск ===
if __name__ == "__main__":
    asyncio.run(main(), debug=True)