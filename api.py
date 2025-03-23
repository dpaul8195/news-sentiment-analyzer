from flask import Flask, request, jsonify, send_file
from utils import get_times_of_india_news
import io

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the News Sentiment Analyzer API"})


@app.route('/analyze', methods=['GET'])
def analyze_news():
    """
    Fetches news, performs sentiment analysis, and returns structured data.
    """
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    news_data = get_times_of_india_news(company, max_articles=10)

    if not news_data:
        return jsonify({"error": "No articles found"}), 404

    # Remove BytesIO object before returning JSON
    if "Audio Bytes" in news_data:
        del news_data["Audio Bytes"]

    return jsonify(news_data)


@app.route('/audio_summary', methods=['GET'])
def get_audio_summary():
    """
    Returns Hindi audio summary as a downloadable mp3 file.
    """
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    news_data = get_times_of_india_news(company, max_articles=10)
    
    if not news_data or "Audio Bytes" not in news_data:
        return jsonify({"error": "Audio summary not available"}), 404

    audio_bytes = news_data["Audio Bytes"]
    return send_file(io.BytesIO(audio_bytes.read()), mimetype="audio/mp3", as_attachment=True, download_name=f"{company}_summary.mp3")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
