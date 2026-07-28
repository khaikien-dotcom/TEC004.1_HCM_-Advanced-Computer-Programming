import os
import re
from google import genai

# Initialize Gemini Client
client = genai.Client()

def predict_market_price(sqm, property_type, current_price):
    """
    Predicts a fair market price for a property in Hanoi using Gemini.
    """
    prompt = (
        f"Act as a Hanoi real estate expert. "
        f"A {property_type} has an area of {sqm} sqm and is listed at {current_price} Billion VND. "
        f"Based on general market trends, predict a fair market price. "
        f"Return ONLY a single float number representing your predicted price in Billions VND. Do not include text."
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",  # <--- Updated model name
        contents=prompt,
    )

    raw_text = response.text.strip()

    try:
        return float(raw_text)
    except ValueError:
        match = re.search(r"[-+]?\d*\.\d+|\d+", raw_text)
        if match:
            return float(match.group())
        raise ValueError(f"Could not convert Gemini response to float: '{raw_text}'")


if __name__ == "__main__":
    dummy_sqm = 85.5
    dummy_type = "Apartment"
    dummy_price = 5.2

    print("--- Running Hanoi Real Estate Price Predictor (Gemini) ---")
    print(f"Property: {dummy_type} | Area: {dummy_sqm} sqm | Listed Price: {dummy_price} Billion VND\n")

    predicted = predict_market_price(dummy_sqm, dummy_type, dummy_price)

    print(f"Predicted Fair Market Price: {predicted} Billion VND")
    print(f"Output Data Type: {type(predicted)}")