# ML model placeholder
from transformers import pipeline
from sklearn.ensemble import IsolationForest

# Load on demand
def get_fraud_classifier():
    return pipeline('sentiment-analysis')  # Default BERT-like; fine-tune later

def get_anomaly_model():
    return IsolationForest(contamination=0.1)