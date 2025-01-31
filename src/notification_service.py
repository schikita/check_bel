import httpx
from config import TELEGRAM_BOT_TOKEN

class NotificationService:
    @staticmethod
    async def _send_telegram_message(chat_id: str, text: str):
        """Отправляет сообщение в Telegram через Bot API."""
        bot_token = TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text,
        }
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status() 
            except httpx.HTTPStatusError as e:
                print(f"Ошибка при отправке сообщения: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
