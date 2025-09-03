# Flask app entry
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blueprints.fraud_detection import fraud_bp
from blueprints.education import education_bp
from blueprints.blockchain import blockchain_bp
from config import Config
from database import Base  # For DB init

app = Flask(__name__)
app.config.from_object(Config)

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)  # Create tables if not exist

# Register blueprints
app.register_blueprint(fraud_bp, url_prefix='/api/fraud')
app.register_blueprint(education_bp, url_prefix='/api/education')
app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')

@app.route('/')
def home():
    return jsonify({"message": "InvestorGuard Backend API"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)