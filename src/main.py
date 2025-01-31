import asyncio
from detect_lang import calculate_language_percentage, get_text_from_url
from notification_service import NotificationService  


THRESHOLD = 5  
USER_IDS = ['505785229', '455011227']


async def monitor_page():
    """Основная функция для мониторинга процента белорусского языка на странице и отправки уведомлений"""
    url_to_check = "https://www.sb.by"

    
    print("Извлекаем текст со страницы...")
    text = get_text_from_url(url_to_check)

    
    print("Рассчитываем процент белорусского языка...")
    result = calculate_language_percentage(text)

    
    message = (
        f"Привет, на сайте {url_to_check} найден процент белорусского языка: {result['bel_percentage']:.2f}%.\n"
        f"Русский: {result['rus_percentage']:.2f}%\n"
        f"Другие (английский, цифры, ошибки): {result['other_percentage']:.2f}%\n"
        f"Слова на белорусском языке: {', '.join(result['bel_words'])}"
    )

    
    print("Отправляем отчет пользователям...")
    for user_id in USER_IDS:
        print(f"Отправка сообщения пользователю {user_id}...")
        try:
            await NotificationService._send_telegram_message(user_id, message)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    
    while True:
        print("Проверка процента...")
        text = get_text_from_url(url_to_check)
        result = calculate_language_percentage(text)

        
        if result['bel_percentage'] >= THRESHOLD:
            print(f"Процент белорусского языка превышает порог: {result['bel_percentage']:.2f}%")
            message = (
                f"На сайте {url_to_check} найден процент белорусского языка: {result['bel_percentage']:.2f}%.\n"
                f"Русский: {result['rus_percentage']:.2f}%\n"
                f"Другие (английский, цифры, ошибки): {result['other_percentage']:.2f}%\n"
                f"Слова на белорусском языке: {', '.join(result['bel_words'])}"
            )
            
            for user_id in USER_IDS:
                print(f"Отправка уведомления пользователю {user_id}...")
                try:
                    await NotificationService._send_telegram_message(user_id, message)
                except Exception as e:
                    print(f"Не удалось отправить уведомление пользователю {user_id}: {e}")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(monitor_page())