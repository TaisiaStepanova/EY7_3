
from transformers import BartForConditionalGeneration, BartTokenizer
from pathlib import Path


def ml(text, min, max):
    # Загрузка предварительно обученной модели BART и токенизатора
    model_name = "facebook/bart-large-cnn"
    model = BartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = BartTokenizer.from_pretrained(model_name)

    # Исходный текст, который вы хотите сжать до резюме
    input_text = """
    Это исходный текст, который вы хотите сжать до резюме. 
    Добавьте здесь всю необходимую информацию и детали.
    """
    #input_text = Path('text.txt', encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')
    #print(input_text)
    # Токенизация и кодирование текста
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True, padding=True)

    # Генерация резюме
    summary_ids = model.generate(inputs["input_ids"], max_length=max, min_length=min, length_penalty=1.0, num_beams=8, early_stopping=True)

    # Декодирование и вывод резюме
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Резюме:")
    print(summary)
    return summary


