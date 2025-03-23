title: News Sentiment Analyzer
emoji: 🐢
colorFrom: blue
colorTo: blue
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false

# News Summarization & Sentiment Analysis with Hindi TTS  
### A Web-Based Tool for Analyzing News Sentiment and Generating Hindi Audio Summaries  

---

## Overview  
This project is a **Flask + Streamlit web application** that:  

- **Extracts news articles** related to a given company (*scraped from Times of India*).  
- **Performs sentiment analysis** using **VADER**.  
- **Extracts key topics** using **RAKE** (*Rapid Automatic Keyword Extraction*).  
- **Provides a comparative sentiment report** across multiple news articles.  
- **Converts the final sentiment summary to Hindi** speech using **gTTS (Google Text-to-Speech)**.  

🚀 **Deployment:** The application is hosted on **Hugging Face Spaces**.  

---

## Project Setup  

### 1. Clone the Repository  
```
git clone https://github.com/yourusername/news-sentiment-analyzer.git
cd news-sentiment-analyzer
```

### 2. Create a Virtual Environment  
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies  
```
pip install -r requirements.txt
```

---

## Running the Application  

### 1. Start the Flask Backend  
```
python api.py
```
✅ The backend will be available at **http://127.0.0.1:5000/**  

### 2. Run the Streamlit Frontend  
Open another terminal and run:  
```
streamlit run app.py
```
✅ The frontend will be available at **http://localhost:8501/**  

---

## API Endpoints  

### 1. API Health Check  
```
GET /health
```
**Response:**  
```
{"status": "API is running"}
```

### 2. Analyze News Sentiment  
```
GET /analyze?company=Tesla
```
**Response:**  
```
{
  "Company": "Tesla",
  "Articles": [
    {
      "Title": "Tesla's New Model Breaks Sales Records",
      "Summary": "Tesla's latest EV sees record sales in Q3...",
      "Sentiment": "Positive",
      "Topics": ["Electric Vehicles", "Stock Market", "Innovation"],
      "Link": "https://timesofindia.indiatimes.com/..."
    }
  ],
  "Comparative Sentiment Score": {
    "Sentiment Distribution": {"Positive": 3, "Negative": 5, "Neutral": 2},
    "Coverage Differences": [
      {
        "Comparison": "Article 1 is about growth, Article 2 is about legal issues.",
        "Impact": "Investors may react positively to growth news but stay cautious about legal issues."
      }
    ],
    "Topic Overlap": {"Common Topics": ["Electric Vehicles"]}
  },
  "Final Sentiment Analysis": "Tesla’s latest news coverage is mostly positive.",
  "Audio": "[Play Hindi Speech]"
}
```

### 3. Get Hindi Audio Summary  
```
GET /audio_summary?company=Tesla
```
📥 **Returns a downloadable MP3 file** with the Hindi summary.  

---

## Technologies Used  

- **Frontend:** Streamlit  
- **Backend:** Flask  
- **Web Scraping:** BeautifulSoup  
- **Sentiment Analysis:** VADER (NLTK)  
- **Topic Extraction:** RAKE (Rapid Automatic Keyword Extraction)  
- **Translation:** Google Translate API  
- **Text-to-Speech (TTS):** gTTS (Google Text-to-Speech)  
- **Deployment:** Hugging Face Spaces  

---

## Deployment on Hugging Face Spaces  

1. **Create a new space** at [Hugging Face Spaces](https://huggingface.co/spaces).  
2. Select **Docker or Python** environment.  
3. Upload all files (`app.py`, `api.py`, `requirements.txt`, etc.).  
4. Modify `api.py` to use:  
```
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
```
5. Add `requirements.txt`:  
```
Flask
streamlit
requests
beautifulsoup4
vaderSentiment
rake-nltk
gtts
googletrans==4.0.0-rc1
```
6. **Push changes** to Hugging Face.  

---

## Troubleshooting  

### Flask API Not Running?  
- Ensure `api.py` is running **before** opening `app.py`.  
- Check with:  
```
curl http://127.0.0.1:5000/health
```

### Streamlit App Not Loading?  
- Ensure Flask is running **before launching Streamlit**.  
- Restart with:  
```
streamlit run app.py
```

### Audio Summary Not Playing?  
- Check if `gTTS` is installed:  
```
pip install gtts
```
- Ensure the `/audio_summary` endpoint is reachable.  

---

## Future Enhancements  
- ✅ **Multi-language support** for translations & speech.  
- ✅ **More robust news scraping** beyond Times of India.  
- ✅ **Real-time sentiment trends** across multiple companies.  

---

## License  
This project is **open-source** under the **MIT License**. Feel free to modify and contribute!  

🔗 **GitHub Repo:** [https://github.com/dpaul8195/news-sentiment-analyzer](https://github.com/dpaul8195/news-sentiment-analyzer)  

---

### 🔥 Built with ❤️ by **Debabrata Paul**  
