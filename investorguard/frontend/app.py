import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

BASE_URL = "http://localhost:5000/api"  # Change if deployed

# --- Enhanced Custom CSS for Modern UI ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: transparent;
        }
        
        /* Header Styling */
        .main-header {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .main-title {
            color: white;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        .main-subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            font-weight: 300;
            margin-top: 0;
        }
        
        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }
        
        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 1rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .metric-label {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Status Indicators */
        .status-safe {
            background: linear-gradient(135deg, #4ade80, #22c55e);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        }
        
        .status-warning {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }
        
        .status-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: 600;
            display: inline-block;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
        }
        
        /* Enhanced Buttons */
        .stButton button {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
            width: 100%;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #1d4ed8, #1e40af);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
        }
        
        /* Input Fields */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            color: white;
            padding: 0.8rem;
        }
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: white !important;
            font-weight: 600 !important;
        }
        
        /* Feature Cards */
        .feature-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            color: white;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .feature-description {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛡️ InvestorGuard</h1>
        <p class="main-subtitle">Advanced AI-Powered Fraud Detection & Investment Education Platform</p>
    </div>
""", unsafe_allow_html=True)

# Enhanced Sidebar with Icons
st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: white;">
        <h2>🎯 Navigation</h2>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["🔍 Fraud Dashboard", "📘 Educational Hub", "📈 Trading Simulator", "🔗 Audit Trail"],
    index=0
)

# Fraud Dashboard
if page == "🔍 Fraud Dashboard":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🚨 Real-Time Fraud Detection System")
    st.markdown("Analyze investment advice and detect potential fraud using advanced AI algorithms")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📝 Content Analysis")
            content = st.text_area(
                "Enter investment advice or advisor content to analyze",
                placeholder="Paste the content you want to analyze for potential fraud...",
                height=150
            )
            platform = st.selectbox("Select Platform", ["X (Twitter)", "Reddit", "Telegram", "WhatsApp", "Other"])
            
            analyze_btn = st.button("🔍 Analyze for Fraud", key="analyze_fraud")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📊 Quick Stats")
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">24,567</div>
                    <div class="metric-label">Cases Analyzed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">89%</div>
                    <div class="metric-label">Accuracy Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">₹2.3Cr</div>
                    <div class="metric-label">Fraud Prevented</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        if analyze_btn and content:
            with st.spinner("🔄 Analyzing content with AI..."):
                time.sleep(2)  # Simulate API call
                # Mock response for demo
                mock_response = {
                    "flagged": True,
                    "confidence": 85.7,
                    "market_anomaly": True,
                    "sebi_status": "Not Registered",
                    "risk_factors": ["Unrealistic returns promised", "Pressure tactics", "Unregistered advisor"]
                }
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("📋 Analysis Results")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    status = "🚨 HIGH RISK" if mock_response['flagged'] else "✅ SAFE"
                    status_class = "status-danger" if mock_response['flagged'] else "status-safe"
                    st.markdown(f'<div class="{status_class}">{status}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{mock_response['confidence']}%</div>
                            <div class="metric-label">Confidence</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    anomaly_status = "⚠️ DETECTED" if mock_response['market_anomaly'] else "✅ NORMAL"
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{anomaly_status}</div>
                            <div class="metric-label">Market Anomaly</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    sebi_class = "status-danger" if mock_response['sebi_status'] == "Not Registered" else "status-safe"
                    st.markdown(f'<div class="{sebi_class}">{mock_response["sebi_status"]}</div>', unsafe_allow_html=True)
                
                # Risk Factors
                st.subheader("⚠️ Risk Factors Identified")
                for factor in mock_response['risk_factors']:
                    st.markdown(f"• {factor}")
                
                # Visualization
                fig = go.Figure(data=[
                    go.Bar(x=['Fraud Risk', 'Market Anomaly', 'SEBI Compliance'], 
                          y=[85.7, 92.3, 15.2],
                          marker_color=['#ef4444', '#f59e0b', '#22c55e'])
                ])
                fig.update_layout(
                    title="Risk Assessment Breakdown",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# Educational Hub
elif page == "📘 Educational Hub":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📚 Interactive Investment Learning")
    st.markdown("Learn about investments, markets, and fraud prevention through interactive tutorials")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📖</div>
                <div class="feature-title">Interactive Tutorials</div>
                <div class="feature-description">Learn investment basics with step-by-step guides</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">AI Chatbot</div>
                <div class="feature-description">Get instant answers to your investment questions</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌍</div>
                <div class="feature-title">Multi-Language</div>
                <div class="feature-description">Learn in Hindi, English, Tamil, and more</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Tutorial Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📖 Get Personalized Tutorial")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("What would you like to learn about?", placeholder="e.g., stock market basics, mutual funds, SIP...")
    with col2:
        language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Marathi", "Bengali"])
    
    if st.button("📚 Generate Tutorial"):
        with st.spinner("🎓 Creating personalized tutorial..."):
            time.sleep(2)
            st.success("📖 Tutorial Generated!")
            st.markdown("""
                <div style="background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 15px; margin: 1rem 0;">
                    <h4>Stock Market Basics - Beginner's Guide</h4>
                    <p>Welcome to the world of investing! The stock market is where shares of publicly traded companies are bought and sold...</p>
                    <ul>
                        <li>🏢 Understanding what stocks represent</li>
                        <li>📈 How stock prices move</li>
                        <li>💰 Different ways to invest</li>
                        <li>⚠️ Common risks to avoid</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chatbot Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🤖 AI Investment Assistant")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_question = st.text_input("Ask me anything about investments...", placeholder="What is SIP? How to identify fraud?")
    
    if st.button("💬 Ask Assistant"):
        if user_question:
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)
                # Mock response
                bot_response = f"Great question! Regarding '{user_question}', here's what you should know: This is a comprehensive answer that would help you understand the concept better. Always remember to invest wisely and avoid get-rich-quick schemes!"
                st.session_state.chat_history.append(("You", user_question))
                st.session_state.chat_history.append(("InvestorGuard AI", bot_response))
    
    # Display chat history
    for role, message in st.session_state.chat_history[-6:]:  # Show last 6 messages
        if role == "You":
            st.markdown(f"**🧑 {role}:** {message}")
        else:
            st.markdown(f"**🤖 {role}:** {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Trading Simulator
elif page == "📈 Trading Simulator":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🎮 Virtual Trading Simulator")
    st.markdown("Practice trading with virtual money in real market conditions")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Portfolio Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">₹1,00,000</div>
                <div class="metric-label">Portfolio Value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">+12.5%</div>
                <div class="metric-label">Total Returns</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">₹25,000</div>
                <div class="metric-label">Available Cash</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Trading Interface
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🛒 Place Virtual Trade")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        stock_symbol = st.text_input("Stock Symbol", placeholder="RELIANCE, TCS, INFY...")
    with col2:
        action = st.selectbox("Action", ["Buy", "Sell"])
    with col3:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    
    if st.button("🎯 Execute Trade"):
        with st.spinner("⚡ Processing trade..."):
            time.sleep(1)
            st.success(f"✅ Successfully {action.lower()}ed {quantity} shares of {stock_symbol}!")
            
            # Show trade result
            st.markdown(f"""
                <div style="background: rgba(34, 197, 94, 0.2); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4>Trade Executed Successfully!</h4>
                    <p>🏢 Stock: {stock_symbol}</p>
                    <p>📊 Action: {action}</p>
                    <p>🔢 Quantity: {quantity}</p>
                    <p>💰 Estimated Value: ₹{quantity * 2500:,}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Performance Chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Portfolio Performance")
    
    # Mock data for chart
    dates = pd.date_range(start='2024-01-01', end='2024-09-01', freq='D')
    portfolio_values = [100000 + i*50 + (i%10)*200 for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=portfolio_values, mode='lines', 
                           name='Portfolio Value', line=dict(color='#22c55e', width=3)))
    fig.update_layout(
        title="Portfolio Growth Over Time",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Audit Trail
elif page == "🔗 Audit Trail":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🔗 Blockchain Audit Trail")
    st.markdown("Immutable record of all transactions and fraud detection activities")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mock blockchain data
    blockchain_data = [
        {"timestamp": "2024-09-03 10:30:15", "type": "Fraud Detection", "status": "Flagged", "hash": "0x7f9a2b..."},
        {"timestamp": "2024-09-03 10:25:42", "type": "Trade Execution", "status": "Success", "hash": "0x3e8f1c..."},
        {"timestamp": "2024-09-03 10:20:18", "type": "SEBI Verification", "status": "Verified", "hash": "0x9d4a7b..."},
        {"timestamp": "2024-09-03 10:15:33", "type": "Fraud Detection", "status": "Safe", "hash": "0x5b2e9f..."}
    ]
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📜 Recent Blockchain Entries")
    
    for entry in blockchain_data:
        status_class = "status-danger" if entry['status'] == "Flagged" else "status-safe"
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>🔗 {entry['type']}</strong><br>
                        <small>⏰ {entry['timestamp']}</small><br>
                        <small>🔐 Hash: {entry['hash']}</small>
                    </div>
                    <div class="{status_class}">{entry['status']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Blockchain Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">45,672</div>
                <div class="metric-label">Total Blocks</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">99.9%</div>
                <div class="metric-label">Uptime</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">2.3s</div>
                <div class="metric-label">Avg Block Time</div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7); margin-top: 3rem;">
        <hr style="border-color: rgba(255,255,255,0.2);">
        <p>🛡️ InvestorGuard - Protecting Your Financial Future | Made with ❤️ in India</p>
        <p>📞 Support: 1800-XXX-XXXX | 📧 help@investorguard.in</p>
    </div>
""", unsafe_allow_html=True)