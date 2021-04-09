from flask import Flask, url_for, render_template, request
import sumy
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
# import gensim
# import gensim_sum_ext
# NLP Packages
from spacy_summarization import text_summarizer
from nltk_summarization import  nltk_summarizer
# from gensim.summarization.summarizer import summarize_corpus

# Other Packages
import spacy
nlp = spacy.load("en_core_web_sm")
import time

# Web Scrapping packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

app=Flask(__name__, static_url_path='/static')

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# FUNCTIONS


# Sumy
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


# Reading Time
def readingTime(mytext):
    total_words = len([ token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime
# Fetch Text From Url
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text, soup.find_all('p')))
    return fetched_text



# FLASK DEVELOPEMENT


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end-start
    return render_template('index.html', ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)


@app.route('/analyze_url', methods=['GET', 'POST'])
def analyze_url():
    start = time.time()
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url)
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end-start
        final_time=round(final_time,2)
    return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)


@app.route('/compare_summary')
def compare_summary():
    return render_template('compare_summary.html')


@app.route('/comparer', methods=["GET", "POST"])
def compare():
    start = time.time()
    if request.method=="POST":
        rawtext=request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary_spacy)

        # Summary for NLTk
        final_summary_nltk = nltk_summarizer(rawtext)
        summary_reading_time_nltk = readingTime(final_summary_nltk)

        # # Summary for gensim
        # final_summary_gensim = summarize(rawtext)
        # summary_reading_time_gensim = readingTime(final_summary_gensim)

        # Summary for Sumy
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)

        end = time.time()
        final_time = end - start





    return render_template('compare_summary.html', ctext=rawtext, final_summary_spacy=final_summary_spacy,#final_summary_gensim=final_summary_gensim
                           final_summary_nltk=final_summary_nltk,
                           final_time=final_time, final_reading_time=final_reading_time,
                           summary_reading_time=summary_reading_time,
                           # summary_reading_time_gensim=summary_reading_time_gensim,
                           final_summary_sumy=final_summary_sumy, summary_reading_time_sumy=summary_reading_time_sumy,
                           summary_reading_time_nltk=summary_reading_time_nltk)


@app.route('/about')
def about():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


