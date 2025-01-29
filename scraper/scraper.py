import requests
from bs4 import BeautifulSoup
from langdetect import detect
from nltk.tokenize import word_tokenize
from nltk import download

# Скачиваем необходимые ресурсы
download('punkt')

# Создание собственного списка стоп-слов для белорусского языка
belarusian_stopwords = {
    'і', 'на', 'я', 'у', 'які', 'для', 'сваі', 'ад', 'пры', 'калі', 'з', 'па', 'не', 'це', 'бы', 'с', 'як', 'аб', 'мы'
}

def preprocess_text(text: str) -> str:
    """Очистка текста (удаление лишних пробелов и специфическая обработка)."""
    text = ' '.join(text.split())
    return text

def calculate_belarusian_percentage(text: str) -> float:
    """Вычисляет процент белорусского языка в тексте."""
    text = preprocess_text(text)
    
    words = word_tokenize(text.lower())
    
    # Убираем стоп-слова
    filtered_words = [word for word in words if word not in belarusian_stopwords]
    
    # Подсчитываем белорусские слова
    belarusian_count = sum(1 for word in filtered_words if detect(word) == 'be')
    
    return (belarusian_count / len(filtered_words)) * 100 if filtered_words else 0

def check_belarusian_language_on_page(url: str) -> float:
    """Проверяет процент белорусского языка на странице"""
    try:
        # Отключаем проверку SSL-сертификатов для тестирования
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        text = soup.get_text()
        return calculate_belarusian_percentage(text)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе страницы: {e}")
        return 0.0
