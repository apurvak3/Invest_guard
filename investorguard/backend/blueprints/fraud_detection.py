# Fraud detection blueprint
from flask import Blueprint, jsonify, request
from models.fraud_model import get_fraud_classifier, get_anomaly_model
import pandas as pd
import yfinance as yf  # Replaced nselib
from utils.scraping import scrape_social_media
from config import Config

fraud_bp = Blueprint('fraud', __name__)

@fraud_bp.route('/detect', methods=['POST'])
def detect_fraud():
    data = request.json
    content = data.get('content', '')
    platform = data.get('platform', 'X')
    
    # NLP analysis
    classifier = get_fraud_classifier()
    result = classifier(content)
    sentiment = result[0]['label']
    score = result[0]['score']
    
    # Mock social data (real scraping needs API keys)
    social_data = scrape_social_media(platform, content)
    
    # Market data (NIFTY 50 via yfinance)
    try:
        nifty = yf.Ticker("^NSEI")  # NIFTY 50 index
        market_data = nifty.history(period="1d")  # Last day's data
        df = pd.DataFrame({'price': [market_data['Close'].iloc[-1]]})  # Latest close price
    except Exception as e:
        df = pd.DataFrame({'price': [1000]})  # Mock fallback
        print(f"yfinance error: {e}")
    
    anomaly_model = get_anomaly_model()
    anomalies = anomaly_model.fit_predict(df[['price']])
    
    # Mock SEBI verify (unchanged)
    advisor = data.get('advisor', '')
    sebi_status = {'verified': True} if advisor else {'verified': False}
    
    flagged = (sentiment == 'NEGATIVE' and score > 0.7) or (anomalies[0] == -1 if len(anomalies) > 0 else False)
    if flagged:
        # Log to blockchain (mock)
        requests.post('http://localhost:5000/api/blockchain/log', json={'content': content})
    
    return jsonify({
        'flagged': flagged,
        'confidence': score,
        'market_anomaly': anomalies[0] == -1 if len(anomalies) > 0 else False,
        'sebi_status': sebi_status,
        'social_data': social_data
    })