import streamlit as st
import requests
import pandas as pd

# Flask backend URL
API_URL = "http://127.0.0.1:5000"

st.set_page_config(layout="wide")  # Better layout handling

st.title("📰 News Sentiment Analyzer")
st.write("Enter a company name to analyze its latest news and sentiment.")

company = st.text_input("🔍 Company Name", "Tesla")

if st.button("Analyze News"):
    with st.spinner("Fetching news..."):
        try:
            # Call Flask API to fetch news analysis
            response = requests.get(f"{API_URL}/analyze?company={company}", timeout=10)
            response.raise_for_status()

            news_data = response.json()

            if "Articles" not in news_data or not news_data["Articles"]:
                st.warning("⚠️ No news articles found for this company. Try another one.")
                st.stop()

            # Display articles
            st.subheader("📰 Latest Articles")
            for idx, article in enumerate(news_data["Articles"], start=1):
                col1, col2 = st.columns([3, 1])  # Title (Left) | Sentiment (Right)
                
                with col1:
                    st.markdown(f"### {idx}. [{article['Title']}]({article['Link']})")
                
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

                # Use expander to hide long summaries
                with st.expander("📖 View Summary"):
                    st.markdown(f"<p style='font-size:14px;'>{article.get('Summary', 'Summary not available.')}</p>", unsafe_allow_html=True)

                st.markdown(f"**📝 Topics:** {', '.join(article.get('Topics', ['No topics found']))}")
                st.write("---")

            # 📊 Comparative Sentiment Score
            st.subheader("📊 Comparative Sentiment Score")

            # 🎯 **Sentiment Distribution as Progress Bars**
            sentiment_scores = news_data.get("Comparative Sentiment Score", {}).get("Sentiment Distribution", {})
            if sentiment_scores:
                st.markdown("### 📈 Sentiment Distribution")
                st.progress(sentiment_scores.get("Positive", 0) / 10.0)
                st.text(f"Positive: {sentiment_scores.get('Positive', 0)} articles")

                st.progress(sentiment_scores.get("Neutral", 0) / 10.0)
                st.text(f"Neutral: {sentiment_scores.get('Neutral', 0)} articles")

                st.progress(sentiment_scores.get("Negative", 0) / 10.0)
                st.text(f"Negative: {sentiment_scores.get('Negative', 0)} articles")

            # 🎯 **Coverage Differences as a Readable Table**
            coverage_differences = news_data.get("Comparative Sentiment Score", {}).get("Coverage Differences", [])

            if coverage_differences:
                st.markdown("### 🔍 Coverage Differences")

                # Convert list of dicts into a DataFrame
                coverage_df = pd.DataFrame(coverage_differences)

                # Format text for better readability
                def wrap_text(text, width=70):
                    return "\n".join([text[i:i+width] for i in range(0, len(text), width)])

                coverage_df = coverage_df.applymap(lambda x: wrap_text(str(x)) if isinstance(x, str) else x)

                # Display full data using st.table() for better readability
                st.table(coverage_df)


            # 🎯 **Topic Overlap with Sorted Article Numbers**
            topic_overlap = news_data.get("Comparative Sentiment Score", {}).get("Topic Overlap", {})

            if topic_overlap:
                st.markdown("### 🔗 Topic Overlap")

                # Display Common Topics
                st.markdown(f"**Common Topics:** {', '.join(topic_overlap.get('Common Topics', []))}")

                # Sort Unique Topics by Article Number
                unique_topics = topic_overlap.get("Unique Topics", {})
                sorted_articles = sorted(unique_topics.keys(), key=lambda x: int(x.split()[-1]))  # Sort by article number

                # Display Unique Topics in Increasing Order
                st.markdown("**Unique Topics per Article:**")
                for article in sorted_articles:
                    st.markdown(f"- **{article}:** {', '.join(unique_topics[article])}")

            # 📌 Final Sentiment Analysis
            st.subheader("📌 Final Sentiment Analysis")
            st.write(news_data.get("Final Sentiment Analysis", "No final analysis available."))

            # 🔊 Fetch & Play Audio
            st.subheader("🔊 Audio Summary in Hindi")
            audio_response = requests.get(f"{API_URL}/audio_summary?company={company}", timeout=10)
            
            if audio_response.status_code == 200:
                st.audio(audio_response.content, format="audio/mp3")
                st.download_button(
                    label="📥 Download Audio",
                    data=audio_response.content,
                    file_name=f"{company}_sentiment_summary.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error("⚠️ Audio summary not available.")

        except requests.exceptions.RequestException:
            st.error("❌ API Connection Error: Unable to reach the backend. Ensure Flask is running.")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")
