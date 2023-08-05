import tkinter as tk
from tkinter import *
import nltk
from textblob import TextBlob
from newspaper import Article
from time import sleep
from newspaper.article import ArticleException, ArticleDownloadState
from googletrans import Translator

# Function to translate text
def translate_text(text, dest):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text

# Add the URL
def summarize():
    url = urltext.get('1.0', "end").strip()
    # Create object called article
    article = Article(url)
    article.download()
    # Download article
    while article.download_state == ArticleDownloadState.NOT_STARTED:
        sleep(1)
    # Parse article
    article.parse()
    article.nlp()
        
    analysis = TextBlob(article.text)
    polarity = analysis.sentiment.polarity
    asentiment = ""
    if polarity > 0:
        asentiment += "positive"
    elif polarity < 0:
        asentiment += "negative"
    else:
        asentiment += "neutral"    

   # print(f'Title: {article.title}')
   # print(f'Authors: {article.authors}')
   # print(f'Publication Date: {article.publish_date}')
   # print(f'Summary: {article.summary}')
    
    # Translate summary to the desired language
    dest_lang = langtext.get('1.0', "end").strip()
    if not dest_lang:
        dest_lang = 'en'  # Set default language to English
    translated_summary = translate_text(article.summary, dest_lang)
    
    title.config(state='normal')
    author.config(state='normal')
    publication.config(state='normal')
    summary.config(state='normal')
    sentiment.config(state='normal')

    title.delete("1.0", "end")
    title.insert("1.0", article.title)

    author.delete("1.0", "end")
    author.insert("1.0", article.authors)

    publication.delete("1.0", "end")
    publication.insert("1.0", article.title)

    summary.delete("1.0", "end")
    summary.insert("1.0", translated_summary)

    sentiment.delete("1.0", "end")
    sentiment.insert("1.0", f"polarity: {polarity} Sentiment: {asentiment}")
                     
    title.config(state='disabled')
    author.config(state='disabled')
    publication.config(state='disabled')
    summary.config(state='disabled')
    sentiment.config(state='disabled')

# GUI Time
root = tk.Tk()
root.title("Cube News Summarizer")
root.geometry('1200x600')

tlabel = tk.Label(root, text="Title")
tlabel.pack()

title = tk.Text(root, height=1, width=140)
title.config(state="disabled", bg='#dddddd')
title.pack()

alabel = tk.Label(root, text="Author")
alabel.pack()

author = tk.Text(root, height=1, width=140)
author.config(state="disabled", bg='#dddddd')
author.pack()

plabel = tk.Label(root, text="Publishing Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state="disabled", bg='#dddddd')
publication.pack()

slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=20, width=140)
summary.config(bg='#dddddd')
summary.pack()

selabel = tk.Label(root, text="Sentiment Analysis")
selabel.pack()

sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state="disabled", bg='#dddddd')
sentiment.pack()

ulabel = tk.Label(root, text="URL")
ulabel.pack()

urltext = tk.Text(root, height=1, width=140)
urltext.config(bg="grey")
urltext.pack()

llabel = tk.Label(root, text="Language (Destination)")
llabel.pack()

langtext = tk.Text(root, height=1, width=140)
langtext.config(bg="grey")
langtext.pack()

btn = tk.Button(root, text="Summarize", command=summarize)
btn.pack()

root.mainloop()
