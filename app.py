from flask import Flask, request, jsonify
from predict import predict

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict_route():
    ticker = request.args.get('ticker', default='AAPL', type=str)
    try:
        predictions, signals = predict(ticker)
        # Convert signals DataFrame to JSON serializable format
        signals_json = signals.fillna(0).to_dict(orient='index')
        predictions_json = predictions.to_dict()
        return jsonify({
            'ticker': ticker,
            'predictions': predictions_json,
            'signals': signals_json
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
