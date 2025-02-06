import fasttext
from pathlib import Path


DATA_DIR = Path('models')
MODEL_PATH = DATA_DIR / 'model_custom_tuned.bin'
model_custom = fasttext.load_model(str(MODEL_PATH))

def detect_language(text: str) -> str:
    """Определяет язык текста (русский или белорусский) с помощью обученной модели."""
    label, _ = model_custom.predict(text)
    return 'rus' if label[0] == '__label__ru' else 'bel'


def calculate_language_percentage(sentences: list) -> dict:
    """Вычисляет процент белорусского и русского языка в списке предложений, а также слова на других языках."""
    rus_count = 0
    bel_count = 0
    bel_words = []  
    processed_words = 0  

    for sentence in sentences:
        processed_words += 1  
        language = detect_language(sentence)
        if language == 'rus':
            rus_count += 1
        else:
            bel_count += 1
            bel_words.append(sentence)  

    if processed_words > 0:
        rus_percentage = (rus_count / processed_words) * 100
        bel_percentage = (bel_count / processed_words) * 100
    else:
        rus_percentage = bel_percentage = 0

    return {
        "rus_percentage": rus_percentage,
        "bel_percentage": bel_percentage,
        "bel_words": bel_words
    }