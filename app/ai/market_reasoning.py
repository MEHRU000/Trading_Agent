"""
Market Reasoning Module.
Constructs structured context prompts for trade candidate validation by Claude AI.
"""

from typing import Dict, Any


def build_analysis_prompt(
    symbol: str,
    direction: str,
    entry: float,
    sl: float,
    tp: float,
    metrics: Dict[str, Any],
    account_balance: float,
    account_equity: float
) -> str:
    """
    Assembles a rich text prompt detailing the technical setup and account state.
    
    Args:
        symbol: Trading instrument (e.g., XAUUSD)
        direction: BUY or SELL
        entry: Planned entry price
        sl: Planned stop loss price
        tp: Planned take profit price
        metrics: Dictionary containing strategy technical indicators
        account_balance: Current account balance
        account_equity: Current account equity
        
    Returns:
        str: Text prompt formatted for Claude
    """
    rsi = metrics.get("rsi", "N/A")
    ema_20 = metrics.get("ema_20", "N/A")
    ema_50 = metrics.get("ema_50", "N/A")
    atr = metrics.get("atr", "N/A")
    volume = metrics.get("volume", "N/A")
    avg_volume = metrics.get("avg_volume", "N/A")
    market_structure = metrics.get("market_structure", "N/A")

    # Math details
    risk_distance = abs(entry - sl)
    reward_distance = abs(tp - entry)
    rr_ratio = reward_distance / risk_distance if risk_distance > 0 else 0.0

    prompt = f"""
Analyze the following trade setup for {symbol} and decide whether it represents a high-quality confluence setup.

--- TRADE SETUP DETAILS ---
Symbol: {symbol}
Action: {direction}
Proposed Entry Price: {entry:.2f}
Stop Loss (SL): {sl:.2f} (Distance: {risk_distance:.2f} points)
Take Profit (TP): {tp:.2f} (Distance: {reward_distance:.2f} points)
Risk-to-Reward Ratio: 1:{rr_ratio:.2f}

--- TECHNICAL METRICS ---
EMA 20: {ema_20}
EMA 50: {ema_50}
EMA Trend state: {"EMA20 is ABOVE EMA50 (Bullish Crossover)" if ema_20 > ema_50 else "EMA20 is BELOW EMA50 (Bearish Crossover)"}
RSI (14): {rsi}
ATR (14): {atr}
Current Candle Volume: {volume}
Average Volume (SMA 20): {avg_volume}
Volume Confirmation: {"Volume is ABOVE average" if volume > avg_volume else "Volume is BELOW average"}
Market Structure Trend: {market_structure}

--- ACCOUNT CONTEXT ---
Account Balance: ${account_balance:,.2f} USD
Account Equity: ${account_equity:,.2f} USD
Risk allocation: 1% per trade

--- RULES FOR VALIDATION ---
You are a quantitative risk analyst. Evaluate the structural quality of this setup:
1. Confluence: Check if indicators align properly with the trade direction.
2. Structure: Ensure the trade is taken in the direction of the dominant market structure.
3. Volatility Check: Verify that the stop loss is set at an appropriate distance relative to the ATR (e.g. >= 1.0 * ATR).
4. Red Flags: Check for signs of weakness (e.g. RSI is overbought (>70) on a buy signal, or oversold (<30) on a sell signal, representing potential exhaustion).
5. Output format: You must return a single JSON string matching:
{{
    "validation": <boolean indicating approval>,
    "confidence_score": <float from 0.0 to 1.0 indicating setup quality>,
    "reasoning": "<concise explanation of reasoning and any red flags detected>"
}}
Do NOT output anything other than the JSON object.
"""
    return prompt.strip()
