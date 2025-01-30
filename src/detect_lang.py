import fasttext
from pathlib import Path
from typing import Literal

DATA_DIR = Path('models')
MODEL_PATH = DATA_DIR / 'model_custom_tuned.bin'

model_custom = fasttext.load_model(str(MODEL_PATH))

def detect_language(text: str) -> Literal["rus", "bel"]:
    """Определяет язык текста (русский или белорусский) с помощью обученной модели."""
    label, _ = model_custom.predict(text)
    return 'rus' if label[0] == '__label__ru' else 'bel'

print(detect_language("Привет, как дела?")) 
print(detect_language("Добры дзень, як справы?")) 
