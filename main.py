import json
import requests
import main_functions
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import streamlit as st
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

#nltk.download("punkt")
#nltk.download("stopwords")



st.title("COP4813 - Web Application Programming")
st.title("Project 1")
st.title("Part A - The Stories API")
st.write("This app uses the Top Stories API to display the most common words "
             "used in the top current articles based on a specified topic selected "
             "by the user. The data is displayed as a line chart and as a wordcloud image.")
st.subheader("I - Topic Selection")

user_name = st.text_input("Please enter your name:")

option = st.selectbox("Please select a topic:",
                      ["", "arts", "automobiles", "books", "business", "fashion",
                      "food", "health", "home", "insider", "magazine", "movies",
                      "nyregion", "obituaries", "opinion", "politics", "realestate",
                      "science", "sports", "sundayreview", "technology", "theater",
                      "t-magazine", "travel", "upshot", "us", "world"])

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict['my_key']
url = "https://api.nytimes.com/svc/topstories/v2/" + option + ".json?api-key=" + api_key
top_stories = requests.get(url).json()
main_functions.save_to_file(top_stories, "JSON_Files/top_stories.json")
top_stories_articles = main_functions.read_from_file("JSON_Files/top_stories.json")

if user_name and (option != ""):
    st.write("Hi " + user_name + "! Your current selection is " + option + ".")


st.subheader("II - Frequency Distribution")

str1 = ""
if st.checkbox("Click here to generate frequency distribution"):
    if option != "":
        for i in top_stories_articles["results"]:
            str1 = str1 + i["abstract"]
        words = word_tokenize(str1)
        words_no_punc = []
        for w in words:
            if w.isalpha():
                words_no_punc.append(w.lower())
        stopwords = stopwords.words("english")
        clean_words = []
        for w in words_no_punc:
            if w not in stopwords:
                clean_words.append(w)
        fdist = FreqDist(clean_words)
        chart_data = pd.DataFrame(fdist.most_common(10), fdist.most_common(10))
        st.line_chart(chart_data)
    else:
        st.write("You have not selected a topic!")


st.subheader("III - Wordcloud")

if st.checkbox("Click here to generate wordcloud"):
    if option != "":
        wordcloud = WordCloud().generate(str1)
        plt.figure(figsize=(7, 7))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig("top_stories_cloud.png")
        image1 = Image.open("top_stories_cloud.png")
        st.image(image1)
    else:
        st.write("You have not selected a topic!")

st.title("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed, or viewed articles.")

option2 = st.selectbox("Please select your preferred set of articles:",
                      ["", "shared", "emailed", "viewed"])

period = st.selectbox("Select the period of time (last days)", ["", "1", "7", "30"])


if (option2 != "") and (period != ""):
    url2 = "https://api.nytimes.com/svc/mostpopular/v2/" + option2 + "/" + period + ".json?api-key=" + api_key
    most_popular = requests.get(url2).json()
    main_functions.save_to_file(most_popular, "JSON_Files/most_popular.json")
    most_popular_articles = main_functions.read_from_file("JSON_Files/most_popular.json")
    str2 = ""
    for i in most_popular_articles["results"]:
        str2 = str2 + i["abstract"]

    wordcloud2 = WordCloud().generate(str2)
    plt.figure(figsize=(7, 7))
    plt.imshow(wordcloud2)
    plt.axis("off")
    plt.savefig("most_popular_cloud.png")
    image2 = Image.open("most_popular_cloud.png")
    st.image(image2)