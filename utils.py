import requests
import random
from io import BytesIO
from bs4 import BeautifulSoup
from gtts import gTTS
from rake_nltk import Rake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import re
import nltk
from collections import Counter


nltk.download('punkt')
nltk.download('stopwords')  # Needed for filtering keywords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Initialize RAKE for keyword extraction
rake = Rake()


def get_news_articles(topic, max_articles_per_source=5):
    all_articles = []

    # --- Source 1: Times of India ---
    toi_url = f"https://timesofindia.indiatimes.com/topic/{topic}"
    try:
        response = requests.get(toi_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="uwU81")[:max_articles_per_source]

        for result in results:
            title_tag = result.find("div", class_="fHv_i o58kM")
            summary_tag = result.find("p", class_="oxXSK o58kM")
            link_tag = result.find("a")
            date_tag = result.find("div", class_="ZxBIG")

            title = title_tag.text.strip() if title_tag else "No title"
            summary = summary_tag.text.strip() if summary_tag else "No summary"
            link = f"https://timesofindia.indiatimes.com{link_tag['href']}" if link_tag else "#"

            formatted_date = "Date not found"
            if date_tag:
                match = re.search(r"/\s+(.*?\(\w+\))", date_tag.get_text())
                if match:
                    date_str = match.group(1).replace("(IST)", "").strip()
                    try:
                        dt = datetime.strptime(date_str, "%b %d, %Y, %H:%M")
                        formatted_date = dt.strftime("%b %d, %Y")
                    except Exception:
                        formatted_date = date_str

            sentiment_score = sia.polarity_scores(f"{title}. {summary}")["compound"]
            sentiment = "Positive" if sentiment_score >= 0.05 else "Negative" if sentiment_score <= -0.05 else "Neutral"
            topics = extract_topics(title + " " + summary)

            all_articles.append({
                "Source": "Times of India",
                "Title": title,
                "Summary": summary,
                "Link": link,
                "Date": formatted_date,
                "Sentiment": sentiment,
                "Topics": topics
            })

    except Exception as e:
        print(f"Error scraping TOI: {e}")

    # --- Source 2: Economic Times ---
    et_url = f"https://economictimes.indiatimes.com/topic/{topic}"
    try:
        response = requests.get(et_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="contentD")[:max_articles_per_source]

        for result in results:
            a_tag = result.find("a", class_="wrapLines l2")
            summary_tag = result.find("p", class_="wrapLines l3")
            time_tag = result.find("time")

            title = a_tag.text.strip() if a_tag else "No title"
            link = f"https://economictimes.indiatimes.com{a_tag['href']}" if a_tag and "href" in a_tag.attrs else "#"
            summary = summary_tag.text.strip() if summary_tag else "No summary"
            date_str = time_tag.text.strip() if time_tag else "Date not found"

            try:
                dt = datetime.strptime(date_str.replace(" IST", ""), "%d %b, %Y, %I:%M %p")
                formatted_date = dt.strftime("%b %d, %Y")
            except Exception:
                formatted_date = date_str

            sentiment_score = sia.polarity_scores(f"{title}. {summary}")["compound"]
            sentiment = "Positive" if sentiment_score >= 0.05 else "Negative" if sentiment_score <= -0.05 else "Neutral"
            topics = extract_topics(title + " " + summary)

            all_articles.append({
                "Source": "Economic Times",
                "Title": title,
                "Summary": summary,
                "Link": link,
                "Date": formatted_date,
                "Sentiment": sentiment,
                "Topics": topics
            })

    except Exception as e:
        print(f"Error scraping Economic Times: {e}")

    
    # Sentiment Distribution
    sentiment_counts = Counter(article["Sentiment"] for article in all_articles)

    # Topic Overlap
    topic_overlap = analyze_topic_overlap(all_articles)

    # Coverage Differences
    coverage_differences = generate_coverage_differences(all_articles)

    # Final Sentiment Summary
    final_sentiment_summary_english = generate_final_sentiment_analysis(sentiment_counts, topic)

    # Translation & TTS
    final_sentiment_summary_hindi = translate_to_hindi(final_sentiment_summary_english)
    audio_bytes = text_to_speech_hindi(final_sentiment_summary_hindi)


    return {
        "Company": topic,
        "Articles": all_articles,
        "Comparative Sentiment Score": {
            "Sentiment Distribution": dict(sentiment_counts),
            "Topic Overlap": topic_overlap,
            "Coverage Differences": coverage_differences  # Can be implemented later
        },
        "Final Sentiment Analysis": final_sentiment_summary_english,
        "Audio Bytes": audio_bytes
    }


def extract_topics(text, max_keywords=3):
    """Extracts key topics using RAKE, filtering out irrelevant keywords."""
    rake.extract_keywords_from_text(text)
    
    keywords = []
    for kw in rake.get_ranked_phrases():
        cleaned_kw = kw.title().strip()
        if (
            len(kw.split()) > 1 and
            "summary available" not in kw.lower() and
            not re.search(r"\b\d+\b", kw) and
            not re.search(r"[^\w\s-]", kw) and
            len(re.sub(r"[^a-zA-Z\s]", "", kw).strip()) > 1 and
            not any(word in stop_words for word in kw.lower().split())
        ):
            keywords.append(cleaned_kw)

    return keywords[:max_keywords] if keywords else ["General News"]



def generate_coverage_differences(articles):
    """Compares three random pairs of articles and generates coverage differences."""
    if len(articles) < 6:
        return [{"Comparison": "Not enough articles to compare 3 pairs.", "Impact": "At least 6 articles required."}]
    
    sampled_indices = random.sample(range(len(articles)), 6)
    pairs = [(sampled_indices[i], sampled_indices[i+1]) for i in range(0, 6, 2)]

    comparisons = []
    for idx1, idx2 in pairs:
        article1 = articles[idx1]
        article2 = articles[idx2]

        title1 = article1['Title'].replace('\n', ' ').strip()
        title2 = article2['Title'].replace('\n', ' ').strip()
        sentiment1 = article1['Sentiment'].strip().lower()
        sentiment2 = article2['Sentiment'].strip().lower()

        comparisons.append({
            "Comparison": f"Article {idx1+1}: '{title1}' vs Article {idx2+1}: '{title2}'.",
            "Impact": f"Article {idx1+1} is {sentiment1}, while Article {idx2+1} is {sentiment2}."
        })

    return comparisons

def analyze_topic_overlap(articles):
    """Finds common and unique topics among articles."""
    if len(articles) < 2:
        return {"Common Topics": [], "Unique Topics": {}}
    
    all_topics = [set(article["Topics"]) for article in articles if article["Topics"]]
    common_topics = set.intersection(*all_topics) if len(all_topics) > 1 else set()
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
    """Fallback translation using pre-defined mappings."""
    translations = {
        "’s latest news coverage is mostly positive. Potential stock growth expected.":
            "की ताज़ा ख़बरों की कवरेज ज्यादातर सकारात्मक है। स्टॉक में वृद्धि की संभावना है।",
        " is facing challenges, with a high number of negative reports. Investors may remain cautious.":
            " चुनौतियों का सामना कर रहा है, कई नकारात्मक रिपोर्टों के साथ। निवेशक सतर्क रह सकते हैं।",
        "'s news sentiment is neutral or mixed. Market response could go either way.":
            "की खबरों की भावना तटस्थ या मिली-जुली है। बाज़ार की प्रतिक्रिया किसी भी दिशा में जा सकती है।"
    }
    for key, val in translations.items():
        if key in text:
            return text.split(key)[0] + val
    return "अनुवाद करने में त्रुटि हुई।"


def text_to_speech_hindi(text):
    """Converts text to Hindi speech using gTTS and returns audio bytes."""
    tts = gTTS(text=text, lang="hi")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer
