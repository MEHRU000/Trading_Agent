"""
Historical Strategy Backtester Engine.
Simulates trading strategy rules on a CSV historical dataset and calculates
win rates, profit factors, Sharpe ratio, and drawdowns.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.strategy.xauusd_strategy import evaluate_strategy
from app.utils.logger import app_logger


class Backtester:
    """
    Simulates historical executions of the XAUUSD strategy rules.
    """
    def __init__(self, start_balance: float = 10000.0, risk_percent: float = 0.01):
        self.start_balance = start_balance
        self.risk_percent = risk_percent

    def run(self, csv_path: str, atr_multiplier: float = 1.5, rr_ratio: float = 2.0) -> Dict[str, Any]:
        """
        Runs strategy simulation over data in CSV.
        CSV format: datetime, open, high, low, close, volume
        """
        app_logger.info(f"Loading backtest historical data from {csv_path}...")
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Historical CSV file not found at: {csv_path}")

        # Load and sanitize data
        df = pd.read_csv(csv_path)
        required_cols = ["open", "high", "low", "close", "volume"]
        for col in required_cols:
            if col not in df.columns:
                # Attempt case-insensitive recovery
                matches = [c for c in df.columns if c.lower() == col]
                if matches:
                    df = df.rename(columns={matches[0]: col})
                else:
                    raise ValueError(f"Missing required CSV column: {col}")

        # Clean datetime column
        date_col = None
        for col in ["datetime", "date", "time"]:
            if col in df.columns:
                date_col = col
                break
        if date_col:
            df["datetime"] = pd.to_datetime(df[date_col])
        else:
            df["datetime"] = pd.date_range(start="2026-01-01", periods=len(df), freq="h")

        df = df.sort_values("datetime").reset_index(drop=True)
        app_logger.info(f"Data loaded successfully. Total candles: {len(df)}")

        # Simulation states
        balance = self.start_balance
        equity = balance
        peak_balance = balance
        max_drawdown = 0.0
        
        trades: List[Dict[str, Any]] = []
        active_trade: Optional[Dict[str, Any]] = None
        
        # Start scanning after enough bars to calculate indicators (min 50 bars lookback)
        start_idx = 50
        
        for i in range(start_idx, len(df)):
            current_bar = df.iloc[i]
            
            # Check if active trade is hit by SL or TP in the current bar
            if active_trade:
                trade_type = active_trade["type"]
                entry = active_trade["entry_price"]
                sl = active_trade["sl"]
                tp = active_trade["tp"]
                volume = active_trade["volume"]
                
                # Check for exit conditions
                # High/Low bounds evaluated
                high = current_bar["high"]
                low = current_bar["low"]
                
                exit_price = None
                exit_reason = ""
                exit_time = current_bar["datetime"]
                
                if trade_type == "BUY":
                    # Check SL first (worst-case assumption)
                    if low <= sl:
                        exit_price = sl
                        exit_reason = "SL Hit 🔴"
                    elif high >= tp:
                        exit_price = tp
                        exit_reason = "TP Hit 🟢"
                else:  # SELL
                    if high >= sl:
                        exit_price = sl
                        exit_reason = "SL Hit 🔴"
                    elif low <= tp:
                        exit_price = tp
                        exit_reason = "TP Hit 🟢"
                        
                if exit_price is not None:
                    # Calculate PnL
                    multiplier = 100.0  # Gold Contract Size
                    if trade_type == "BUY":
                        pnl = (exit_price - entry) * volume * multiplier
                    else:
                        pnl = (entry - exit_price) * volume * multiplier
                        
                    balance += pnl
                    equity = balance
                    
                    # Update drawdown
                    peak_balance = max(peak_balance, balance)
                    dd = (peak_balance - balance) / peak_balance if peak_balance > 0 else 0.0
                    max_drawdown = max(max_drawdown, dd)

                    active_trade["exit_price"] = exit_price
                    active_trade["exit_time"] = exit_time
                    active_trade["profit"] = pnl
                    active_trade["reason"] = exit_reason
                    active_trade["final_balance"] = balance
                    
                    trades.append(active_trade)
                    active_trade = None
                    continue  # Move to next bar after exit
            
            # Evaluate new signal if no trade is active
            if active_trade is None:
                # Pass historical slice up to current index
                history_slice = df.iloc[i - 49 : i + 1]
                
                # Evaluate strategy
                result = evaluate_strategy(history_slice, atr_multiplier=atr_multiplier, rr_ratio=rr_ratio)
                signal = result["signal"]
                
                if signal != "NONE":
                    entry = result["entry_price"]
                    sl = result["sl_price"]
                    tp = result["tp_price"]
                    
                    # Calculate dynamic lot size (1% risk)
                    risk_amount = balance * self.risk_percent
                    sl_dist_points = abs(entry - sl) * 100.0
                    
                    if sl_dist_points > 0:
                        raw_lots = risk_amount / (sl_dist_points * 1.00)
                        # Conform rounding (0.01 step)
                        vol = round(round(raw_lots / 0.01) * 0.01, 2)
                        vol = max(0.01, vol)
                    else:
                        vol = 0.01
                        
                    active_trade = {
                        "ticket": len(trades) + 1,
                        "type": signal,
                        "entry_time": current_bar["datetime"],
                        "entry_price": entry,
                        "sl": sl,
                        "tp": tp,
                        "volume": vol,
                        "metrics": result["metrics"]
                    }
                    
        # If trade remains open at end, close at last bar price
        if active_trade:
            last_bar = df.iloc[-1]
            exit_p = last_bar["close"]
            entry = active_trade["entry_price"]
            vol = active_trade["volume"]
            
            multiplier = 100.0
            if active_trade["type"] == "BUY":
                pnl = (exit_p - entry) * vol * multiplier
            else:
                pnl = (entry - exit_p) * vol * multiplier
                
            balance += pnl
            active_trade["exit_price"] = exit_p
            active_trade["exit_time"] = last_bar["datetime"]
            active_trade["profit"] = pnl
            active_trade["reason"] = "END OF BACKTEST"
            active_trade["final_balance"] = balance
            trades.append(active_trade)

        # Compute Metrics
        total_trades = len(trades)
        if total_trades == 0:
            return {"total_trades": 0, "net_profit": 0.0}
            
        wins = [t["profit"] for t in trades if t["profit"] > 0]
        losses = [t["profit"] for t in trades if t["profit"] <= 0]
        
        win_count = len(wins)
        loss_count = len(losses)
        win_rate = (win_count / total_trades) * 100.0 if total_trades > 0 else 0.0
        
        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else (gross_profit if gross_profit > 0 else 1.0)
        
        net_profit = balance - self.start_balance
        
        # Sharpe Ratio (daily equivalent)
        trade_returns = [t["profit"] / self.start_balance for t in trades]
        std_dev = np.std(trade_returns)
        mean_return = np.mean(trade_returns)
        sharpe = (mean_return / std_dev) * np.sqrt(total_trades) if std_dev > 0 else 0.0

        summary = {
            "start_balance": self.start_balance,
            "final_balance": round(balance, 2),
            "net_profit": round(net_profit, 2),
            "roi_pct": round((net_profit / self.start_balance) * 100.0, 2),
            "total_trades": total_trades,
            "wins": win_count,
            "losses": loss_count,
            "win_rate_pct": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "max_drawdown_pct": round(max_drawdown * 100.0, 2),
            "sharpe_ratio": round(sharpe, 2),
            "trades_list": trades
        }
        
        app_logger.info(
            f"Backtest Finished. ROI: {summary['roi_pct']}% | Win Rate: {summary['win_rate_pct']}% "
            f"| Profit Factor: {summary['profit_factor']} | Max DD: {summary['max_drawdown_pct']}%"
        )
        
        return summary
