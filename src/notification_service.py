import httpx
from config import TELEGRAM_BOT_TOKEN

class NotificationService:
    @staticmethod
    async def notify_admin(telegram_id: str, site_url: str, bel_percentage: float, threshold: float):
        """Уведомление администратора, если процент белорусского языка превышает порог."""
        
        # Формируем текст уведомления
        text = (
            f"На сайте {site_url} найден процент белорусского языка: {bel_percentage:.2f}%.\n"
        )
        
        # Если процент белорусского языка превышает порог, уведомляем администратора
        if bel_percentage >= threshold:
            text += f"Внимание! Процент белорусского языка на странице превышает установленный порог {threshold}%."
        
        await NotificationService._send_telegram_message(telegram_id, text)

    @staticmethod
    async def _send_telegram_message(chat_id: str, text: str):
        """Отправляет сообщение в Telegram через Bot API."""
        bot_token = TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()  # Проверяем на ошибки в ответе
            except httpx.HTTPStatusError as e:
                print(f"Ошибка при отправке сообщения: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
