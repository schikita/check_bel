import fasttext
import numpy as np
import random
from pathlib import Path
from texts import belarusian_texts, russian_texts

# Папка для хранения файлов
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

MODEL_PATH = DATA_DIR / 'model_custom_tuned.bin'

def split_data(texts, train_ratio=0.8):
    random.shuffle(texts)
    split_index = int(len(texts) * train_ratio)
    return texts[:split_index], texts[split_index:]

def prepare_data(file_path: Path, texts, label):
    with file_path.open('w', encoding='utf-8') as f:
        for text in texts:
            f.write(f'__label__{label} {text}\n')

# Разделяем данные автоматически
belarusian_train, belarusian_test = split_data(belarusian_texts)
russian_train, russian_test = split_data(russian_texts)

prepare_data(DATA_DIR / 'belarusian_train.txt', belarusian_train, 'be')
prepare_data(DATA_DIR / 'russian_train.txt', russian_train, 'ru')
prepare_data(DATA_DIR / 'belarusian_test.txt', belarusian_test, 'be')
prepare_data(DATA_DIR / 'russian_test.txt', russian_test, 'ru')

def merge_files(input_files, output_file: Path):
    with output_file.open('w', encoding='utf-8') as outfile:
        for fname in input_files:
            with fname.open('r', encoding='utf-8') as infile:
                outfile.write(infile.read())

merge_files([
    DATA_DIR / 'belarusian_train.txt',
    DATA_DIR / 'russian_train.txt'
], DATA_DIR / 'train.txt')

merge_files([
    DATA_DIR / 'belarusian_test.txt',
    DATA_DIR / 'russian_test.txt'
], DATA_DIR / 'test.txt')

model_pretrained = fasttext.load_model('lid.176.ftz')

model_custom_default = fasttext.train_supervised(
    input=str(DATA_DIR / 'train.txt'),
    lr=0.1,
    epoch=25,
    wordNgrams=2
)

model_custom_tuned = fasttext.train_supervised(
    input=str(DATA_DIR / 'train.txt'),
    lr=1.0,
    epoch=100,
    wordNgrams=4,
    bucket=500000, 
    dim=300,
    minn=2, 
    maxn=6,  
    loss='hs' 
)

# Сохраняем модель
model_custom_tuned.save_model(str(MODEL_PATH))

def evaluate_model(model, test_file: Path, is_pretrained=False):
    correct = 0
    total = 0
    
    with test_file.open('r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) < 2:
                continue
            label, text = parts
            
            if is_pretrained:
                labels, probs = model.predict(text)
                probs = np.array(probs, dtype=np.float64, copy=True)
            else:
                labels, probs = model.predict(text)
                probs = np.array(probs, dtype=np.float64, copy=True)
            
            pred = labels[0].replace('__label__', '')
            
            if pred == label.replace('__label__', ''):
                correct += 1
            total += 1
    
    return correct / total if total > 0 else 0

def predict_text(text, model_path=MODEL_PATH):
    model = fasttext.load_model(str(model_path))
    label, prob = model.predict(text)
    return label[0].replace('__label__', ''), prob[0]

test_file_path = DATA_DIR / 'test.txt'
accuracy_pretrained = evaluate_model(model_pretrained, test_file_path, is_pretrained=True)
accuracy_custom_default = evaluate_model(model_custom_default, test_file_path)
accuracy_custom_tuned = evaluate_model(model_custom_tuned, test_file_path)

print(f'Pre-trained model accuracy: {accuracy_pretrained:.2f}')
print(f'Custom model (default) accuracy: {accuracy_custom_default:.2f}')
print(f'Custom model (tuned) accuracy: {accuracy_custom_tuned:.2f}')

sample_text = "Привет, как дела?"
label, confidence = predict_text(sample_text)
print(f'Text: "{sample_text}"\nPredicted Label: {label}, Confidence: {confidence:.2f}')

