from detect_lang import detect_language, calculate_language_percentage, get_text_from_url


url_to_check = "https://www.sb.by"  # Укажите URL для проверки
text = get_text_from_url(url_to_check)  # Извлекаем текст со страницы
calculate_language_percentage(text)  # Рассчитываем проценты и выводим белорусские слова  