from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import re

app = Flask(__name__)
CORS(app)

def analyze_feedback(feedback):
    analysis = TextBlob(feedback)
    sentiment_score = analysis.sentiment.polarity
    
    if sentiment_score > 0.2:
        sentiment = "Positive"
        sentiment_class = "sentiment-positive"
    elif sentiment_score < -0.2:
        sentiment = "Negative"
        sentiment_class = "sentiment-negative"
    else:
        sentiment = "Neutral"
        sentiment_class = "sentiment-neutral"
    
    themes = {
        'room': ['room', 'bed', 'pillow', 'linen', 'housekeeping'],
        'staff': ['staff', 'reception', 'concierge', 'service', 'manager'],
        'facilities': ['pool', 'gym', 'spa', 'restaurant', 'breakfast', 'wifi'],
        'cleanliness': ['clean', 'dirty', 'hygiene', 'towel', 'toilet'],
        'value': ['price', 'expensive', 'cheap', 'worth', 'value']
    }
    
    detected_themes = []
    for theme, keywords in themes.items():
        if any(re.search(rf'\b{kw}\b', feedback.lower()) for kw in keywords):
            detected_themes.append(theme)
    
    recommendations = []
    if "Negative" in sentiment:
        if 'room' in detected_themes:
            recommendations.append("1. Inspect and improve room maintenance procedures")
        if 'staff' in detected_themes:
            recommendations.append("2. Conduct additional staff training sessions")
        if 'cleanliness' in detected_themes:
            recommendations.append("3. Review housekeeping protocols and quality checks")
    
    if not recommendations and "Positive" in sentiment:
        recommendations.append("1. Maintain current service standards")
        recommendations.append("2. Recognize staff for their good work")
    
    return {
        "sentiment": sentiment,
        "sentiment_class": sentiment_class,
        "score": sentiment_score,
        "themes": detected_themes,
        "recommendations": recommendations
    }

@app.route('/analyze', methods=['POST'])
def analyze():
    feedback = request.json.get('feedback', '')
    if not feedback:
        return jsonify({"error": "No feedback provided"}), 400
    
    return jsonify(analyze_feedback(feedback))

if __name__ == '__main__':
    app.run(debug=True)