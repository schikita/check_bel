from scraper.scraper import check_belarusian_language_on_page
from bot.bot import send_notification
import time

# Порог для отправки уведомлений
THRESHOLD = 10  

def monitor_page(url: str):
    """Мониторит страницу и отправляет уведомления, если процент белорусского языка превышает порог"""
    while True:
        percentage = check_belarusian_language_on_page(url)
        if percentage >= THRESHOLD:
            send_notification(f"На странице {url} найдено {percentage:.2f}% белорусского языка.")
        time.sleep(60)

if __name__ == "__main__":
    url_to_check = "https://www.sb.by"
    monitor_page(url_to_check)
