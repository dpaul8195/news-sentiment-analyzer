---
title: News Sentiment Analyzer
emoji: 🐢
colorFrom: blue
colorTo: blue
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
---
# News Summarization & Sentiment Analysis with Hindi TTS
### A Web-Based Tool for Analyzing News Sentiment and Generating Hindi Audio Summaries

---

## Overview
This project is a Streamlit web application that:

- Scrapes news articles related to a given company (from Times of India and Economic Times)
- Performs sentiment analysis using VADER
- Extracts key topics using RAKE (Rapid Automatic Keyword Extraction)
- Provides a comparative sentiment report across multiple news articles
- Generates a Hindi audio summary using gTTS (Google Text-to-Speech)

Deployment: The application is compatible with Hugging Face Spaces and Render

---

## Project Setup

1. Clone the Repository
$ git clone https://github.com/dpaul8195/news-sentiment-analyzer.git
$ cd news-sentiment-analyzer

2. Create a Virtual Environment
$ python -m venv venv

To activate:
- On Linux/macOS:
$ source venv/bin/activate
- On Windows:
$ venv\Scripts\activate

3. Install Dependencies
$ pip install -r requirements.txt

---

## Running the Application

$ streamlit run app.py

The frontend will be available at: http://localhost:8501/

---

## Technologies Used

- Frontend: Streamlit
- Web Scraping: BeautifulSoup
- Sentiment Analysis: VADER (NLTK)
- Topic Extraction: RAKE (RAKE-NLTK)
- Text-to-Speech (TTS): gTTS
- Translation: (Fallback) Hindi mapping for sentiment
- Deployment: Hugging Face Spaces

---

## requirements.txt

streamlit
pandas
matplotlib
beautifulsoup4
requests
gTTS
rake-nltk
vaderSentiment
nltk

---

## Future Enhancements

- Add more news sources
- Live sentiment dashboard for multiple companies
- Multilingual audio support
- Real-time trend charts

---

## License
This project is licensed under the MIT License.

GitHub Repo: https://github.com/dpaul8195/news-sentiment-analyzer

---

Built with ❤️ by Debabrata Paul
