from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(amount)
    print(type(amount))
    print(source_currency)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * float(cf)
    final_amount = round(final_amount, 2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }

    return jsonify(response)

def fetch_conversion_factor(source,target):

    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey=R2K2IWRNU77H608I".format(source,target)

    response = requests.get(url)
    response = response.json()
    print(response['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    print(type(response['Realtime Currency Exchange Rate']['5. Exchange Rate']))
    return response['Realtime Currency Exchange Rate']['5. Exchange Rate']

if __name__ == "__main__":
    app.run(debug=True)