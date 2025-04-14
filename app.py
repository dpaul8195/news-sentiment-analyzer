import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_news_articles
from datetime import datetime


st.set_page_config(layout="wide")

st.title("📰 News Sentiment Analyzer")
st.write("Enter a company name to analyze its latest news and sentiment.")

company = st.text_input("🔍 Company Name", "Tesla").strip().title()


def plot_sentiment_distribution(scores):
    labels = list(scores.keys())
    values = [scores[k] for k in labels]
    colors = ['green', 'red', 'gray']

    fig, ax = plt.subplots()
    ax.barh(labels, values, color=colors)
    ax.set_xlabel("Number of Articles")
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

def parse_date_string(date_str):
    """Convert raw date string to a datetime object (fallback to None if fails)."""
    try:
        return datetime.strptime(date_str, "%b %d, %Y")
    except Exception:
        return None



if st.button("Analyze News"):
    with st.spinner("Fetching news..."):
        try:
            news_data = get_news_articles(company)

            if not news_data or "Articles" not in news_data or not news_data["Articles"]:
                st.warning("⚠️ No news articles found for this company. Try another one.")
                st.stop()

            # Display articles
            st.subheader("📰 Latest Articles")
            for idx, article in enumerate(news_data["Articles"], start=1):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {idx}. [{article['Title']}]({article['Link']})")
                    st.markdown(f"📅 **Published on:** {article['Date']}")
                
                with col2:
                    sentiment_color = {
                        "Positive": "green",
                        "Negative": "red",
                        "Neutral": "gray"
                    }.get(article.get("Sentiment", "Neutral"), "gray")

                    st.markdown(
                        f"<p style='color:{sentiment_color}; font-weight:bold; font-size:16px;'>"
                        f"📊 {article.get('Sentiment', 'Unknown')}</p>",
                        unsafe_allow_html=True
                    )

                with st.expander("📖 View Summary"):
                    st.markdown(
                        f"<p style='font-size:14px;'>{article.get('Summary', 'Summary not available.')}</p>",
                        unsafe_allow_html=True
                    )

                st.markdown(f"**📝 Topics:** {', '.join(article.get('Topics', ['No topics found']))}")
                st.write("---")

            # Comparative Sentiment Score
            st.subheader("📊 Comparative Sentiment Score")
            sentiment_scores = news_data.get("Comparative Sentiment Score", {}).get("Sentiment Distribution", {})
            if sentiment_scores:
                plot_sentiment_distribution(sentiment_scores)


            # Coverage Differences
            coverage_differences = news_data.get("Comparative Sentiment Score", {}).get("Coverage Differences", [])
            if coverage_differences:
                st.markdown("### 🔍 Coverage Differences")
                coverage_df = pd.DataFrame(coverage_differences)

                def wrap_text(text, width=70):
                    return "\n".join([text[i:i+width] for i in range(0, len(text), width)])

                coverage_df = coverage_df.applymap(lambda x: wrap_text(str(x)) if isinstance(x, str) else x)
                st.table(coverage_df)

            # Topic Overlap
            topic_overlap = news_data.get("Comparative Sentiment Score", {}).get("Topic Overlap", {})
            if topic_overlap:
                st.markdown("### 🔗 Topic Overlap")
                st.markdown(f"**Common Topics:** {', '.join(topic_overlap.get('Common Topics', []))}")
                unique_topics = topic_overlap.get("Unique Topics", {})
                sorted_articles = sorted(unique_topics.keys(), key=lambda x: int(x.split()[-1]))
                st.markdown("**Unique Topics per Article:**")
                for article in sorted_articles:
                    st.markdown(f"- **{article}:** {', '.join(unique_topics[article])}")

            # Final Sentiment Analysis
            st.subheader("📌 Final Sentiment Analysis")
            st.write(news_data.get("Final Sentiment Analysis", "No final analysis available."))

            # Audio Summary
            st.subheader("🔊 Audio Summary in Hindi")
            audio_data = news_data.get("Audio Bytes")
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
                st.download_button(
                    label="📥 Download Audio",
                    data=audio_data,
                    file_name=f"{company}_sentiment_summary.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error("⚠️ Audio summary not available.")

        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")


