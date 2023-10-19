import nltk
from pathlib import Path
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from nltk import *
from nltk.corpus import stopwords
from string import punctuation
import tkinter as tk
import math
import spacy.lang.en as English
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
# from gensim.summarization.summarizer import summarize
# from rake_nltk import Rake
from langdetect import detect_langs
from test import *
from summa import keywords
import yake

import nltk

nltk.download('stopwords')

nlp_ru = spacy.load("ru_core_news_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")
doc_name = ""
text = ""
result = ""

root = Tk()
root.title("Super-Duper Fast Resume")
# root.bg['blue']
root['background'] = '#f8e8fa'
space0 = Label(root, text='\n')
aboutButton = Button(root, text='About', width=8, height=2, bg='#f8adff')
space1 = Label(root, text='\n')
chooseDocButton = Button(root, text='Choose doc', width=55, height=2, bg='#f8adff')
space2 = Label(root, text='\n')
resultText = tk.Text(root, state='disabled', width=80, height=20)
space3 = Label(root, text='\n')
detectButton = Button(root, text='Get key words and summarize', width=55, height=2, bg='#f8adff')
space4 = Label(root, text='\n')
saveButton = Button(root, text='Save', width=55, height=2, bg='#f8adff')
space5 = Label(root, text='\n')


def nameOf(path):
    return Path(path).stem


def chooseDocsClicked():
    global doc_name, text, resultText
    resultText.delete('1.0', tk.END)
    resultText.delete(1.0, tk.END)
    resultText.delete("1.0", "end-1c")
    files = filedialog.askopenfilename(multiple=False)
    splitlist = root.tk.splitlist(files)
    for doc in splitlist:
        doc_name = nameOf(doc)
        text = Path(doc, encoding="UTF-8", errors='ignore').read_text(encoding="UTF-8", errors='ignore')


def extract_keywords_from(text):
    if 'en' in str(detect_langs(text)):
        doc = nlp_en(text)
        kw_extractor = yake.KeywordExtractor(
            lan="en",  # язык
            n=3,  # максимальное количество слов в фразе
            dedupLim=0.3,  # порог похожести слов
            top=15  # количество ключевых слов
        )
        keywords = kw_extractor.extract_keywords(text)
    elif 'es' in str(detect_langs(text)):
        doc = nlp_es(text)
        kw_extractor = yake.KeywordExtractor(
            lan="es",  # язык
            n=3,  # максимальное количество слов в фразе
            dedupLim=0.3,  # порог похожести слов
            top=15  # количество ключевых слов
        )
        keywords = kw_extractor.extract_keywords(text)

    print(keywords)

    #keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    #top_keywords = set(sorted(keywords, key=keywords.count, reverse=True)[:40])
    return ', '.join([i[0] for i in keywords])


    # text_clean = ""
    # for i in text.split():
    #     if i not in stops:
    #         text_clean += i + " "
    # keywords.keywords(text_clean, language="russian").split("\n")


    # return ', '.join(top_keywords)


def get_essay(text):
    sentences = []
    for sentence in nltk.sent_tokenize(text):
        terms = []
        for term in nltk.word_tokenize(sentence):
            if term not in punctuation and term not in stopwords.words('spanish') and term not in stopwords.words(
                    'english'):
                terms.append(term)
        sentences.append(terms)
    scores = []
    for sentence in sentences:
        score = 0
        for term in sentence:
            score += ((sentence.count(term) / len(sentence)) * 0.5 * (
                    1 + ((sentence.count(term) / len(sentence)) / (max_freq(sentence)))) * math.log(
                len(sentences) / term_count(term, sentences)))
        scores.append(score)
    essay = ""
    for _ in range(int(len(sentences) / 3)):
        current_max = max(scores)
        for i in range(len(scores) - 1):
            if scores[i] == current_max:
                essay += nltk.sent_tokenize(text)[i]
                scores[i] = 0

                break
    if len(essay) == 0:
        essay += "The text is too short."
    return essay


def max_freq(sentence):
    result = 0
    for term in sentence:
        result = max(result, sentence.count(term))
    return result / len(sentence)


def term_count(term, sentences):
    result = 0
    for sentence in sentences:
        if term in sentence:
            result += 1
    return result


def detectClicked():
    resultText.delete(1.0, END)
    global result
    result = f"Doc: {doc_name}\n"
    result += "--- KEY WORDS: ---\n"
    result += extract_keywords_from(text)
    result += "\n\n--- ESSAY: ---\n"
    result += get_essay(text)
    result += "\n\n--- ML: ---\n"
    result += ml(text, int(len(text.split())/4), int(len(text.split())/3))
    # result += "\n------------------\n"
    resultText.configure(state='normal')
    resultText.insert('end', result)


def saveClicked():
    file = open(doc_name + '_result.txt', 'w', encoding="utf8")
    file.write(result)
    file.close()


def aboutButtonClicked():
    messagebox.showinfo("Lab 3",
                        "Для генерации краткого содержания текста выберите файл, используя Choose doc, далее нажмите на кнопку Get key words and summarize.\nДля сохранения результата нажмите кнопку Save.")


if __name__ == "__main__":
    aboutButton.config(command=aboutButtonClicked)
    chooseDocButton.config(command=chooseDocsClicked)
    detectButton.config(command=detectClicked)
    saveButton.config(command=saveClicked)

    space0.pack()
    aboutButton.pack()
    space1.pack()
    chooseDocButton.pack()
    space2.pack()
    resultText.pack()
    space3.pack()
    detectButton.pack()
    space4.pack()
    saveButton.pack()
    space5.pack()
    root.mainloop()
