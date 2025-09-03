# Education blueprint
from flask import Blueprint, jsonify, request
from transformers import pipeline
import yfinance as yf  # Replaced mock BSE
import random

education_bp = Blueprint('education', __name__)

# Default generator (use smaller model for speed)
generator = pipeline('text-generation', model='gpt2')  # Change to Llama if GPU available

@education_bp.route('/tutorial', methods=['POST'])
def get_tutorial():
    data = request.json
    topic = data.get('topic', 'stocks')
    language = data.get('language', 'English')
    prompt = f"Explain {topic} in simple {language} for beginners."
    response = generator(prompt, max_length=200, num_return_sequences=1)[0]['generated_text']
    return jsonify({'tutorial': response})

@education_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    query = data.get('query', '')
    language = data.get('language', 'English')
    prompt = f"Answer in {language}: {query}"
    response = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
    return jsonify({'response': response})

@education_bp.route('/simulate_trade', methods=['POST'])
def simulate_trade():
    data = request.json
    stock = data.get('stock', 'RELIANCE.NS')  # Default to Reliance (NSE ticker)
    action = data.get('action', 'Buy')
    # Fetch real stock data via yfinance
    try:
        ticker = yf.Ticker(stock)
        stock_data = ticker.history(period="1d")
        simulated_price = stock_data['Close'].iloc[-1]  # Latest close
        # Add slight randomness for simulation
        simulated_price += random.uniform(-0.05 * simulated_price, 0.05 * simulated_price)
    except Exception as e:
        simulated_price = random.uniform(100, 2000)  # Mock fallback
        print(f"yfinance error: {e}")
    return jsonify({'result': f"{action} {stock} at {simulated_price:.2f}", 'price': simulated_price})