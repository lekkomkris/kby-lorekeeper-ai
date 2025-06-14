import os
# D:\my_api\app.py

from flask import Flask, request


def perform_calculation(value):
    """
    Separates the core business logic into its own function.
    This makes it easier to read, test, and reuse.
    """
    if value > 50:
        multiplier = 1.2
        offset = 10
    else:
        multiplier = 1.5
        offset = 5
    return (value * multiplier) + offset


app = Flask(__name__)


@app.route('/calculate')
def calculate():
    """Handles the web request and response."""
    value = int(request.args.get('value', 1))
    result = perform_calculation(value)

    response_data = {
        "original_value": value,
        "documentation": "Calculates a new value based on our algorithm.",
        "result": result
    }
    return response_data


if __name__ == '__main__':
    app.run(debug=True)