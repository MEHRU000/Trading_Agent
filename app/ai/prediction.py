"""app/ai/prediction.py

Simple AI prediction placeholder.
In a real implementation this would call an LLM (Claude, OpenAI, Gemini) to predict the next price
based on market data, indicators, and account balance/equity.
"""

from typing import Dict, Any
from app.utils.config import settings


def predict_price(symbol: str, direction: str, candles: list, metrics: dict, balance: float, equity: float) -> Dict[str, Any]:
    """Return a predicted price and confidence score.

    For now this uses a very simple heuristic: take the last close price and adjust
    it by 0.1% in the direction of the signal. The confidence is a fixed high value.
    """
    if not candles:
        raise ValueError("No candle data available for prediction")
    last_close = candles[-1]["close"] if isinstance(candles[-1], dict) else candles[-1].close
    # Simple delta based on direction
    delta = 0.001 if direction.upper() == "BUY" else -0.001
    predicted_price = last_close * (1 + delta)
    return {
        "predicted_price": round(predicted_price, 5),
        "confidence": 0.92,
        "reason": "Simple heuristic prediction based on last close price",
    }
