from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import random
import os


EPOCHS = {
    "ancient": "Древняя Русь (IX–XIII вв.)",
    "mongol": "Монголо-татарское иго (XIII–XV вв.)",
    "moscow": "Московское царство (XV–XVI вв.)",
    "romanov": "Династия Романовых (1613–1917)",
    "revolution": "Революции и Гражданская война (1917–1922)",
    "ussr": "Советский Союз (1922–1991)",
    "ww2": "Великая Отечественная война (1941–1945)",
    "perestroika": "Перестройка и распад СССР (1985–1991)",
    "modern": "Современная Россия (1991–наст. время)"
}

FACTS_DIR = "facts"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот по истории России \n\nНапиши /help, чтобы узнать список доступных эпох.\n\n⚠️ Внимание: представленные факты основаны на открытых источниках и могут содержать неточности или устаревшую информацию. Авторы бота не несут ответственности за возможные ошибки, интерпретации или последствия, связанные с их использованием.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Доступные эпохи:\n"
    for key, name in EPOCHS.items():
        message += f"/fact {key} — {name}\n"
    await update.message.reply_text(message)

async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажи эпоху. Пример: /fact romanov")
        return

    epoch = context.args[0].lower()
    if epoch not in EPOCHS:
        await update.message.reply_text("Такой эпохи нет. Напиши /help чтобы узнать доступные.")
        return

    file_path = os.path.join(FACTS_DIR, f"{epoch}.json")
    try:
        with open(file_path, encoding="utf-8") as file:
            facts = json.load(file)
        fact = random.choice(facts)
        #print(facts)
        await update.message.reply_text(f"🧠 {fact['title']}\n\n{fact['text']}\n\nИсточник: {fact.get('source', 'не указан')}")
    except Exception as e:
        await update.message.reply_text("Ошибка при чтении фактов.")

def main():
    application = ApplicationBuilder().token("7782322579:AAGVklzYac2RJEHl1kripSbH9PHhv2rChLs").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("fact", fact))
    print("Бот запущен.")
    application.run_polling()

if __name__ == "__main__":
    main()
