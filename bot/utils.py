import telebot
from bot.config import API_TOKEN  # Укажите ваш API_TOKEN

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)

def send_notification(message: str, chat_id: str):
    """Отправка уведомления в Telegram"""
    bot.send_message(chat_id, message)
