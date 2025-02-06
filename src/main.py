import asyncio
from typing import NoReturn
from detect_lang import calculate_language_percentage
from notification_service import NotificationService
from text_extractor import ExtractionConfig, TextExtractor
from config import THRESHOLD, USER_IDS, DEBUG


async def monitor_page() -> NoReturn:
    """Основная функция для мониторинга процента белорусского языка на странице и отправки уведомлений"""
    url_to_check = "https://www.sb.by"

    additional_texts = []
    if DEBUG:
        additional_texts.append("Лукашэнка зацвердзіў Дзяржаўную інвестыцыйную праграму на 2025 год")
        additional_texts.append("Гэта тэставае паведамленне на беларускай мове")

    config1 = ExtractionConfig(
        url=url_to_check,
        container={
            "tag": "div",
            "attrs": {"class": "col-12 col-lg-9 order-1 supertop"},
        },
        child_tag="span",
        child_attrs={"class": "card-title"},
        additional_texts=additional_texts,
    )
    config_aside_news = ExtractionConfig(
        url=url_to_check,
        container={"tag": "ul", "attrs": {"class": "list-group wsNews"}},
        child_tag="span",
        child_attrs={"class": "text"},
        additional_texts=[],
    )

    while True:
        print("Проверка процента...")

        extractor = TextExtractor(configs=[config1, config_aside_news])
        text = extractor.extract_text()
        result = calculate_language_percentage(text)
        if result["bel_percentage"] >= THRESHOLD:
            print(
                f"Процент белорусского языка превышает порог: {result['bel_percentage']:.2f}%"
            )
            bel_words_text = "\n".join(result["bel_words"]) if result["bel_words"] else "Не найден"

            message = (
                f"Анализ сайта {url_to_check}\n"
                f"Процент белорусского языка: {result['bel_percentage']:.2f}%.\n"
                f"Русский: {result['rus_percentage']:.2f}%\n\n"
                f"Белорусский контент: {bel_words_text}"
            )

            for user_id in USER_IDS:
                print(f"Отправка уведомления пользователю {user_id}...")
                try:
                    await NotificationService._send_telegram_message(user_id, message)
                except Exception as e:
                    print(
                        f"Не удалось отправить уведомление пользователю {user_id}: {e}"
                    )

        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(monitor_page())
