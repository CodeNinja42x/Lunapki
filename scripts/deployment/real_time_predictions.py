import pandas as pd
import joblib
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    data = pd.read_csv('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/data/real_time_data.csv')
    model = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/optimized_model.pkl')
    scaler = joblib.load('/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/models/scaler.pkl')
    
    data_scaled = scaler.transform(data)
    predictions = model.predict(data_scaled)
    
    return jsonify(predictions.tolist())

if __name__ == "__main__":
    app.run(debug=True)
