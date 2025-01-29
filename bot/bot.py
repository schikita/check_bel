import telebot
from bot.config import API_TOKEN
from bot.utils import send_notification
import time
import requests

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)

# Глобальная переменная для порога
threshold = 10  # Стартовый порог (по умолчанию 10%)

# Проверяемую страницу
url_to_check = "https://www.sb.by"  # Укажите URL для проверки

@bot.message_handler(commands=['set_threshold'])
def set_threshold(message):
    """Устанавливаем новый порог через команду бота"""
    global threshold
    try:
        # Получаем новый порог из сообщения
        new_threshold = int(message.text.split()[1])
        if 0 <= new_threshold <= 100:
            threshold = new_threshold
            bot.reply_to(message, f"Порог успешно установлен на {threshold}%")
        else:
            bot.reply_to(message, "Порог должен быть в пределах от 0 до 100.")
    except (IndexError, ValueError):
        bot.reply_to(message, "Неверный формат. Используйте: /set_threshold <новый_порог>.")

@bot.message_handler(commands=['check_percentage'])
def check_percentage(message):
    """Проверяем текущий процент белорусского языка на странице"""
    from scraper.scraper import check_belarusian_language_on_page  # Переместили импорт сюда
    percentage = check_belarusian_language_on_page(url_to_check)
    bot.reply_to(message, f"Текущий процент белорусского языка на странице {url_to_check}: {percentage:.2f}%.")
    
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я помогу мониторить процент белорусского языка на страницах. "
                           "Используй команды: \n"
                           "/set_threshold <порог> - установить порог для уведомлений\n"
                           "/check_percentage - проверить текущий процент белорусского языка на странице")

# Функция для мониторинга страницы
def monitor_page():
    """Мониторим страницу и отправляем уведомления, если процент белорусского языка превышает порог"""
    while True:
        from scraper.scraper import check_belarusian_language_on_page  # Переместили имп
