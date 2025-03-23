import requests
import random
from io import BytesIO
from bs4 import BeautifulSoup
from gtts import gTTS
from rake_nltk import Rake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import re

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Initialize RAKE for keyword extraction
rake = Rake()


def extract_topics(text, max_keywords=3):
    """Extracts key topics using RAKE, filtering out irrelevant keywords."""
    rake.extract_keywords_from_text(text)
    
    keywords = [
        kw.title().strip() 
        for kw in rake.get_ranked_phrases()
        if len(kw.split()) > 1  # Ensure multi-word topics
        and "summary available" not in kw.lower()  # Remove irrelevant text
        and not re.search(r"\b\d+\b", kw)  # Remove standalone numbers
        and not re.search(r"[^\w\s-]", kw)  # Remove only symbols like ",", ".", etc.
        and len(re.sub(r"[^a-zA-Z\s]", "", kw).strip()) > 1  # Ensure actual words exist
    ]
    
    return keywords[:max_keywords] if keywords else ["General News"]

def get_times_of_india_news(topic, max_articles=10):
    """Scrapes Times of India for news articles, performs sentiment analysis, and generates a report."""
    search_url = f"https://timesofindia.indiatimes.com/topic/{topic}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for idx, result in enumerate(soup.find_all("div", class_="uwU81")[:max_articles], start=1):
        try:
            link_tag = result.find("a")
            title_tag = result.find("div", class_="fHv_i o58kM")
            summary_tag = result.find("p", class_="oxXSK o58kM")

            title = title_tag.text.strip() if title_tag else "No title available"
            link = f"https://timesofindia.indiatimes.com{link_tag['href']}" if link_tag and "href" in link_tag.attrs else "No link available"
            summary = summary_tag.text.strip() if summary_tag else "No summary available"
            if len(summary) == 0:
                summary = "No summary available"

            text_to_analyze = f"{title}. {summary}"
            sentiment_score = sia.polarity_scores(text_to_analyze)["compound"]
            sentiment = "Positive" if sentiment_score >= 0.05 else "Negative" if sentiment_score <= -0.05 else "Neutral"

            sentiment_counts[sentiment] += 1
            topics = extract_topics(f"{title} {summary}")
            
            articles.append({"Title": title, "Summary": summary, "Sentiment": sentiment, "Topics": topics, "Link": link})
        
        except Exception as e:
            print(f"Skipping an article due to error: {e}")

    coverage_differences = generate_coverage_differences(articles)
    topic_overlap = analyze_topic_overlap(articles)
    final_sentiment_summary_english = generate_final_sentiment_analysis(sentiment_counts, topic)
    final_sentiment_summary_hindi = translate_to_hindi(final_sentiment_summary_english)
    audio_bytes = text_to_speech_hindi(final_sentiment_summary_hindi)

    return {
        "Company": topic,
        "Articles": articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts,
            "Coverage Differences": coverage_differences,
            "Topic Overlap": topic_overlap
        },
        "Final Sentiment Analysis": final_sentiment_summary_english,
        "Audio Bytes": audio_bytes
    }


def generate_coverage_differences(articles):
    """Compares two random articles and generates coverage differences."""
    if len(articles) < 2:
        return [{"Comparison": "Not enough articles to compare.", "Impact": "More data needed."}]
    
    idx1, idx2 = random.sample(range(len(articles)), 2)
    article1, article2 = articles[idx1], articles[idx2]

    return [{
        "Comparison": f"Article {idx1+1}: '{article1['Title']}' vs Article {idx2+1}: '{article2['Title']}'.",
        "Impact": f"Article {idx1+1} is {article1['Sentiment'].lower()}, while Article {idx2+1} is {article2['Sentiment'].lower()}."
    }]


def analyze_topic_overlap(articles):
    """Finds common and unique topics among articles."""
    if len(articles) < 2:
        return {"Common Topics": [], "Unique Topics": {}}
    
    all_topics = [set(article["Topics"]) for article in articles if article["Topics"]]
    common_topics = set.intersection(*all_topics) if all_topics else set()
    unique_topics = {f"Article {idx+1}": list(set(article["Topics"]) - common_topics) for idx, article in enumerate(articles)}

    return {"Common Topics": list(common_topics), "Unique Topics": unique_topics}


def generate_final_sentiment_analysis(sentiment_counts, company_name):
    """Generates a final summary based on sentiment distribution."""
    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        return f"{company_name}’s latest news coverage is mostly positive. Potential stock growth expected."
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        return f"{company_name} is facing challenges, with a high number of negative reports. Investors may remain cautious."
    else:
        return f"{company_name}'s news sentiment is neutral or mixed. Market response could go either way."


def translate_to_hindi(text):
    """Dynamically translates English sentiment statements to Hindi."""
    translator = Translator()
    try:
        return translator.translate(text, src="en", dest="hi").text
    except Exception:
        return "अनुवाद करने में त्रुटि हुई।"


def text_to_speech_hindi(text):
    """Converts text to Hindi speech using gTTS and returns audio bytes."""
    tts = gTTS(text=text, lang="hi")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer
