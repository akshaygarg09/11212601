from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

window_size = 10
window_prev_state = []
window_curr_state = []

def fetch_numbers(number_type):
    url = f"http://testserver.com/numbers/{number_type}"
    try:
        start_time = time.time()
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200 and time.time() - start_time <= 0.5:
            numbers = response.json().get("numbers", [])
            return list(set(numbers))  # Ensure unique numbers
    except requests.RequestException:
        pass
    return []

@app.route('/numbers/<number_type>', methods=['GET'])
def get_average(number_type):
    global window_prev_state, window_curr_state

    if number_type not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number type"}), 400

    numbers = fetch_numbers(number_type)
    window_prev_state = window_curr_state[:]

    for num in numbers:
        if len(window_curr_state) >= window_size:
            window_curr_state.pop(0)  # Remove the oldest number
        window_curr_state.append(num)

    avg = sum(window_curr_state) / len(window_curr_state) if window_curr_state else 0

    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": numbers,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=9876)
