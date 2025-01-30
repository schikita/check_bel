import httpx
import json
import asyncio
import concurrent.futures
from pathlib import Path
from deep_translator import GoogleTranslator
from asyncio import Semaphore

BASE_URL = "http://zn.by/api/v1/news/"
PAGE_SIZE = 100 
TOTAL_PAGES = 100 
OUTPUT_FILE = Path("news_data_translated.json")
CONCURRENT_REQUESTS = 30 
TRANSLATION_CONCURRENT_REQUESTS = 50 

executor = concurrent.futures.ThreadPoolExecutor(max_workers=TRANSLATION_CONCURRENT_REQUESTS)

translation_counter = 0  

def translate_text(text, source_lang='ru', target_lang='be'):
    """Перевод текста с русского на белорусский с обработкой ошибок."""
    global translation_counter
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        translation_counter += 1
        if translation_counter % 10 == 0:
            print(f"Переведено {translation_counter} текстов")
        return translated
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return None

async def translate_batch(texts):
    """Асинхронный перевод текста в потоках."""
    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(executor, translate_text, text) for text in texts if text]
    return await asyncio.gather(*tasks)

async def fetch_page(client, url, semaphore):
    """Асинхронный запрос страницы с ограничением по семафору."""
    async with semaphore:
        try:
            response = await client.get(url, timeout=10, follow_redirects=True)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

async def fetch_news_data(semaphore):
    """Асинхронный сбор данных с параллельной обработкой страниц."""
    news_data = {"ru": [], "be": []}
    url = f"{BASE_URL}?ordering=-creation_at&page_size={PAGE_SIZE}"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = []
        for _ in range(TOTAL_PAGES):
            tasks.append(fetch_page(client, url, semaphore))
            response = await fetch_page(client, url, semaphore)
            if response:
                url = response.get("next")
            if not url:
                break

        pages = await asyncio.gather(*tasks)

        ru_texts = []
        for data in pages:
            if not data:
                continue

            for item in data.get("results", []):
                title_ru = item.get("title")
                summary_ru = item.get("summary")

                if title_ru and summary_ru:
                    ru_texts.extend([title_ru, summary_ru])
                    news_data["ru"].extend([title_ru, summary_ru])
        
        be_texts = await translate_batch(ru_texts)
        news_data["be"].extend([text for text in be_texts if text])
    
    return news_data

def save_to_json(data, file_path):
    """Сохранение данных в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def main():
    """Основная асинхронная функция."""
    semaphore = Semaphore(CONCURRENT_REQUESTS)
    news_data = await fetch_news_data(semaphore)
    save_to_json(news_data, OUTPUT_FILE)
    print(f"Сохранено {len(news_data['ru'])} новостей в {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())