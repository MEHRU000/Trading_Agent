"""
AI Trade Predictor Engine.
Uses recent M15 candlestick data and technical indicators to predict trade setup levels (Entry, SL, TPs).
Interfaces with Anthropic Claude / AWS Bedrock, with a rule-based indicator engine fallback.
"""

import json
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from app.utils.config import settings
from app.utils.logger import app_logger
from app.broker.mt5_connector import mt5_connector
from app.strategy.indicators import add_all_indicators

# Initialize AI clients locally for predictor feature
anthropic_client = None
bedrock_client = None

try:
    if settings.CLAUDE_API_KEY:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        app_logger.info("Predictor: Anthropic client initialized.")
except ImportError:
    app_logger.warning("Predictor: Anthropic SDK not installed.")

try:
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        import boto3
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        app_logger.info("Predictor: AWS Bedrock client initialized.")
except Exception as e:
    app_logger.warning(f"Predictor: Failed to initialize AWS Bedrock client: {e}")


def run_rule_based_fallback(df: pd.DataFrame, bid: float, ask: float, timeframe: str = "M15") -> Dict[str, Any]:
    """
    Local rule-based fallback predictor when Claude AI is unavailable/fails.
    """
    app_logger.info(f"Running local rule-based technical analysis fallback for AI Predictor ({timeframe}).")
    
    # Calculate indicators if not already in dataframe
    if "ema_20" not in df.columns:
        df = add_all_indicators(df)
        
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    
    close = float(last_row["close"])
    ema20 = float(last_row["ema_20"])
    ema50 = float(last_row["ema_50"])
    rsi = float(last_row["rsi_14"])
    atr = float(last_row["atr_14"])
    
    prev_ema20 = float(prev_row["ema_20"])
    prev_ema50 = float(prev_row["ema_50"])
    
    # Basic gold ATR buffer
    atr_buffer = max(atr, 2.0)
    
    # Crossover signals
    bullish_crossover = (prev_ema20 <= prev_ema50) and (ema20 > ema50)
    bearish_crossover = (prev_ema20 >= prev_ema50) and (ema20 < ema50)
    
    # Trend alignment
    bullish_trend = ema20 > ema50
    bearish_trend = ema20 < ema50
    
    # RSI filters
    rsi_bullish = rsi > 50 and rsi < 70
    rsi_bearish = rsi < 50 and rsi > 30
    
    if (bullish_crossover or (bullish_trend and rsi_bullish)) and close > ema20:
        action = "BUY"
        concept = "EMA Trend Crossover"
        entry = ask
        sl = entry - (1.5 * atr_buffer)
        tp1 = entry + (1.5 * atr_buffer)
        tp2 = entry + (3.0 * atr_buffer)
        confidence = 0.78 if bullish_crossover else 0.72
        reasoning = (
            f"Technical Crossover Buy Alert: EMA20 ({ema20:.2f}) is crossing/above EMA50 ({ema50:.2f}) on {timeframe} chart. "
            f"RSI is supportive at {rsi:.1f}. ATR based stop distance is set at {1.5 * atr_buffer:.2f}."
        )
    elif (bearish_crossover or (bearish_trend and rsi_bearish)) and close < ema20:
        action = "SELL"
        concept = "EMA Trend Crossover"
        entry = bid
        sl = entry + (1.5 * atr_buffer)
        tp1 = entry - (1.5 * atr_buffer)
        tp2 = entry - (3.0 * atr_buffer)
        confidence = 0.78 if bearish_crossover else 0.72
        reasoning = (
            f"Technical Crossover Sell Alert: EMA20 ({ema20:.2f}) is crossing/below EMA50 ({ema50:.2f}) on {timeframe} chart. "
            f"RSI is supportive at {rsi:.1f}. ATR based stop distance is set at {1.5 * atr_buffer:.2f}."
        )
    else:
        action = "HOLD"
        concept = "Sideways Consolidation"
        entry = (bid + ask) / 2.0
        sl = entry - (1.5 * atr_buffer)
        tp1 = entry + (1.5 * atr_buffer)
        tp2 = entry + (3.0 * atr_buffer)
        confidence = 0.50
        reasoning = (
            f"Market consolidation observed. EMA20 ({ema20:.2f}) and EMA50 ({ema50:.2f}) are sideways. "
            f"RSI is neutral at {rsi:.1f}. No clear crossover or breakout trigger exists, recommendation is HOLD."
        )
        
    return {
        "action": action,
        "concept": concept,
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "confidence": confidence,
        "reasoning": reasoning
    }


def predict_next_trade(db=None, count: int = 40, timeframe: str = "M15") -> Dict[str, Any]:
    """
    Predicts the next trade setup based on historical candles and AI or technical fallback rules.
    """
    try:
        # 1. Fetch candles
        app_logger.info(f"AI Trade Predictor: Fetching historical rates ({timeframe}) from broker...")
        df = mt5_connector.get_candles("XAUUSD", timeframe, count)
        
        if df is None or len(df) < 20:
            app_logger.error("AI Trade Predictor: Insufficient candlestick data fetched from MT5 connector.")
            return {
                "action": "HOLD",
                "concept": "Error: Data Fetch Failure",
                "entry": 2000.0,
                "sl": 1990.0,
                "tp1": 2015.0,
                "tp2": 2025.0,
                "confidence": 0.0,
                "reasoning": "Error: Failed to fetch recent chart data from the broker terminal. No prediction can be generated."
            }
            
        # 2. Fetch current ticker prices
        tick_data = mt5_connector.get_tick_data("XAUUSD")
        if tick_data:
            bid, ask = tick_data
        else:
            # Fallback to last close
            last_close = float(df.iloc[-1]["close"])
            bid, ask = last_close - 0.15, last_close + 0.15
            
        # 3. Add indicators
        df = add_all_indicators(df)
        
        # 4. Attempt AI prediction if enabled
        if settings.AI_VALIDATION_ENABLED and (anthropic_client or bedrock_client):
            try:
                # Format candle data for Claude prompt
                candles_summary = []
                for _, row in df.tail(15).iterrows():
                    candles_summary.append({
                        "time": str(row.get("datetime", row.get("time"))),
                        "open": float(row["open"]),
                        "high": float(row["high"]),
                        "low": float(row["low"]),
                        "close": float(row["close"]),
                        "volume": int(row["volume"]),
                        "ema20": float(row["ema_20"]),
                        "ema50": float(row["ema_50"]),
                        "rsi": float(row["rsi_14"]),
                        "atr": float(row["atr_14"])
                    })
                    
                prompt = (
                    f"You are an expert algorithmic trading system predicting XAUUSD (Gold) intraday trading decisions on {timeframe} timeframe.\n"
                    f"Current Bid price: {bid:.2f}, Ask price: {ask:.2f}.\n"
                    f"Recent candlestick data (last 15 bars, most recent last):\n"
                    f"{json.dumps(candles_summary, indent=2)}\n\n"
                    f"Requirements:\n"
                    f"1. Choose a trade setup action: BUY (if strong bullish momentum/confluence), SELL (if strong bearish momentum/confluence), or HOLD (if rangebound/neutral/unsafe).\n"
                    f"2. Core trading concept/strategy category (e.g. 'EMA Trend Crossover', 'Mean Reversion Support', 'Breakout Continuation', 'Sideways Consolidation').\n"
                    f"3. If BUY/SELL: Calculate entry (near current ask for buy, bid for sell), sl (approx 1.5x-2.5x ATR away from entry, or $2.00-$6.00 range), tp1 (1:1.5 risk/reward), tp2 (1:2.0+ risk/reward).\n"
                    f"4. If HOLD: Set action to HOLD, and still suggest a hypothetical entry (current mid price), sl, tp1, tp2 for reference.\n"
                    f"5. Provide a confidence level between 0.0 and 1.0 (BUY/SELL should only be suggested if confidence >= 0.70).\n"
                    f"6. Provide a brief professional technical reasoning.\n"
                    f"Respond ONLY with a valid raw JSON object matching this schema exactly:\n"
                    f"{{\n"
                    f"  \"action\": \"BUY\" | \"SELL\" | \"HOLD\",\n"
                    f"  \"concept\": \"string\",\n"
                    f"  \"entry\": float,\n"
                    f"  \"sl\": float,\n"
                    f"  \"tp1\": float,\n"
                    f"  \"tp2\": float,\n"
                    f"  \"confidence\": float,\n"
                    f"  \"reasoning\": \"string\"\n"
                    f"}}\n"
                    f"Do not include markdown blocks, backticks, or introduction text."
                )
                
                system_instruction = (
                    "You are an expert quantitative trading AI analyst. "
                    "Analyze the candlestick sequences, technical indicators, and price actions. "
                    "Provide a precise JSON trade prediction. Respond ONLY with raw JSON."
                )
                
                raw_response = ""
                if settings.AI_PROVIDER == "anthropic" and anthropic_client:
                    response = anthropic_client.messages.create(
                        model=settings.CLAUDE_MODEL_ID,
                        max_tokens=1000,
                        system=system_instruction,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2
                    )
                    raw_response = response.content[0].text
                elif settings.AI_PROVIDER == "bedrock" and bedrock_client:
                    body = json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1000,
                        "system": system_instruction,
                        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                        "temperature": 0.2
                    })
                    model_id = f"anthropic.{settings.CLAUDE_MODEL_ID}"
                    response = bedrock_client.invoke_model(modelId=model_id, body=body)
                    response_body = json.loads(response.get("body").read())
                    raw_response = response_body["content"][0]["text"]
                
                # Parse JSON response
                clean_response = raw_response.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response[7:]
                if clean_response.endswith("```"):
                    clean_response = clean_response[:-3]
                clean_response = clean_response.strip()
                
                data = json.loads(clean_response)
                
                # Prepare response dict
                response = {
                    "action": str(data["action"]).upper(),
                    "concept": str(data.get("concept", "AI Prediction")),
                    "entry": round(float(data["entry"]), 2),
                    "sl": round(float(data["sl"]), 2),
                    "tp1": round(float(data["tp1"]), 2),
                    "tp2": round(float(data["tp2"]), 2),
                    "confidence": round(float(data["confidence"]), 2),
                    "reasoning": str(data["reasoning"])
                }

                # Attempt automatic order placement if enabled and confidence sufficient
                order_executed = False
                order_ticket = None
                order_message = None
                try:
                    if (
                        settings.AI_ORDER_EXECUTION_ENABLED
                        and response["action"] in ("BUY", "SELL")
                        and response["confidence"] >= settings.AI_PREDICTION_CONFIDENCE_THRESHOLD
                    ):
                        order_type = mt5_connector.api.ORDER_TYPE_BUY if response["action"] == "BUY" else mt5_connector.api.ORDER_TYPE_SELL
                        order_req = {
                            "action": mt5_connector.api.TRADE_ACTION_DEAL,
                            "symbol": "XAUUSD",
                            "volume": settings.DEFAULT_TRADE_VOLUME,
                            "price": response["entry"],
                            "sl": response["sl"],
                            "tp": response["tp1"],
                            "type": order_type,
                            "magic": settings.MT5_MAGIC_NUMBER,
                            "comment": f"AI_{response['concept']}"
                        }
                        order_res = mt5_connector.api.order_send(order_req)
                        if getattr(order_res, "retcode", None) == mt5_connector.api.TRADE_RETCODE_DONE:
                            order_executed = True
                            order_ticket = getattr(order_res, "order", None)
                            order_message = getattr(order_res, "comment", None)
                except Exception as oe:
                    app_logger.error(f"AI order placement failed: {oe}")

                # Append order execution info to response
                response.update({
                    "order_executed": order_executed,
                    "order_ticket": order_ticket,
                    "order_message": order_message,
                })
                return response
            except Exception as ai_err:
                app_logger.warning(f"AI prediction engine call failed: {ai_err}. Falling back to rule-engine.")
                
        # 5. Fallback rule-engine execution
        return run_rule_based_fallback(df, bid, ask, timeframe=timeframe)
        
    except Exception as e:
        app_logger.error(f"Error in predict_next_trade: {e}")
        return {
            "action": "HOLD",
            "concept": "Critical Exception",
            "entry": 2000.0,
            "sl": 1990.0,
            "tp1": 2015.0,
            "tp2": 2025.0,
            "confidence": 0.0,
            "reasoning": f"Critical Predictor Exception: {str(e)}"
        }
