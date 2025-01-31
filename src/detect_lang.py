import fasttext
from pathlib import Path
import string
import requests
from bs4 import BeautifulSoup
import ssl
import certifi

ssl_context = ssl.create_default_context(cafile=certifi.where())

# Загрузка модели fasttext
DATA_DIR = Path('models')
MODEL_PATH = DATA_DIR / 'model_custom_tuned.bin'
model_custom = fasttext.load_model(str(MODEL_PATH))

def detect_language(text: str) -> str:
    """Определяет язык текста (русский или белорусский) с помощью обученной модели."""
    label, _ = model_custom.predict(text)
    return 'rus' if label[0] == '__label__ru' else 'bel'

def get_text_from_url(url: str) -> str:
    """Извлекает текст со страницы, удаляя HTML-теги."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    text = soup.get_text(separator=' ')
    return text

def is_valid_word(word: str) -> bool:
    """Проверка, является ли слово допустимым для анализа (исключаем знаки препинания и символы)."""
    return word not in string.punctuation and word.isalpha()  

def calculate_language_percentage(text: str) -> dict:
    """Вычисляет процент белорусского и русского языка в тексте, а также количество слов на других языках."""
    words = text.split() 
    rus_count = 0
    bel_count = 0
    other_count = 0 
    bel_words = []  
    processed_words = 0  

    
    for word in words:
        
        if is_valid_word(word):
            processed_words += 1  
            language = detect_language(word)
            if language == 'rus':
                rus_count += 1
            elif language == 'bel':
                bel_count += 1
                bel_words.append(word)  
            else:
                other_count += 1  
    
    
    if processed_words > 0:
        rus_percentage = (rus_count / processed_words) * 100
        bel_percentage = (bel_count / processed_words) * 100
        other_percentage = (other_count / processed_words) * 100
        
        
        return {
            "rus_percentage": rus_percentage,
            "bel_percentage": bel_percentage,
            "other_percentage": other_percentage,
            "bel_words": bel_words  
        }
    else:
        return {
            "rus_percentage": 0,
            "bel_percentage": 0,
            "other_percentage": 0,
            "bel_words": [] 
        }
