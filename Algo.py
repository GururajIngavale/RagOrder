import pandas as pd
import numpy as np
import mplfinance as mpf


# 1) Load & clean CSV (skiprows=2 as you used)
df = pd.read_csv("Gold_History.csv", skiprows=2, parse_dates=['Datetime'], index_col='Datetime')


# 2) Rename columns to standard OHLCV (your CSV had unnamed columns)
#    Adjust this list to match the order in your file if different.
df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]


# 3) Compute indicators (no spaces in column names)
df['SMA_20'] = df['Close'].rolling(window=20).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()


# 4) Build boolean signal: True when SMA_20 > SMA_50 (in-trend)
df['signal_bool'] = df['SMA_20'] > df['SMA_50']


# 5) Detect crossovers (entries/exits)
# entry = True when signal becomes True (False -> True)
# exit  = True when signal becomes False (True -> False)
df['signal_prev'] = df['signal_bool'].shift(1).fillna(False)
df['entry'] = (df['signal_bool'] == True) & (df['signal_prev'] == False)
df['exit']  = (df['signal_bool'] == False) & (df['signal_prev'] == True)


# NOTE: In real trading you'd enter on NEXT candle open after a crossover.
# If you want that, shift entry/exit by 1: df['entry'] = df['entry'].shift(1)


# 6) Create marker series for plotting: place buy marker slightly below low, sell slightly above high
df['buy_marker']  = np.where(df['entry'], df['Low'] * 0.995, np.nan)
df['sell_marker'] = np.where(df['exit'],  df['High'] * 1.005, np.nan)


# 7) Make addplots for mplfinance
buy_plot = mpf.make_addplot(df['buy_marker'],  type='scatter', marker='^', markersize=60, color='g')
sell_plot = mpf.make_addplot(df['sell_marker'], type='scatter', marker='v', markersize=60, color='r')


# 8) Quick backtest: simple long-only trades entered on entry, exited on exit.
trades = []
position = False
entry_price = None
entry_time = None


for idx, row in df.iterrows():
    if row['entry'] and not position:
        # Enter long at close (or better: next open)
        position = True
        entry_price = row['Close']
        entry_time = idx
    elif row['exit'] and position:
        exit_price = row['Close']
        exit_time = idx
        pnl = exit_price - entry_price
        trades.append({
            'entry_time': entry_time,
            'exit_time': exit_time,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'pnl': pnl
        })
        position = False
        entry_price = None
        entry_time = None

## -------------------------------------------------------------------

# # --- Build equity curve indexed by time ---
# equity_curve = pd.Series(0.0, index=df.index)  # start with 0
# cum_pnl = 0.0


# for t in trades:
#     cum_pnl += t['pnl']
#     equity_curve.loc[t['exit_time']] = cum_pnl


# # forward-fill equity between trades
# equity_curve = equity_curve.ffill().fillna(0)


# # --- Compute drawdown series ---
# running_max = equity_curve.cummax()
# drawdown_series = (equity_curve - running_max) / running_max


## -------------------------------------------------------------------
# --- Yearly Performance with Max Drawdown in $ ---
trades_df = pd.DataFrame(trades)

if not trades_df.empty:
    trades_df['year'] = trades_df['exit_time'].dt.year
    yearly_stats = []

    for year, group in trades_df.groupby('year'):
        # Equity curve in dollars for the year
        equity = group['pnl'].cumsum()

        # Running max equity
        running_max = equity.cummax()

        # Dollar drawdowns (current equity - peak equity)
        drawdowns = equity - running_max

        # Max drawdown (most negative drop)
        max_dd_dollars = drawdowns.min() if not drawdowns.empty else 0.0

        wins = sum(group['pnl'] > 0)
        losses = sum(group['pnl'] <= 0)

        yearly_stats.append({
            'year': year,
            'wins': wins,
            'losses': losses,
            'max_drawdown_dollars': max_dd_dollars
        })

    # Print yearly stats
    print("\nYearly Performance:")
    for stat in yearly_stats:
        print(f"{stat['year']} -> Wins: {stat['wins']} | Losses: {stat['losses']} | Max DD: {stat['max_drawdown_dollars']:.2f} $")

## -------------------------------------------------------------------

# If still in position at end, you can close at last price (optional)
if position:
    exit_price = df['Close'].iloc[-1]
    exit_time = df.index[-1]
    pnl = exit_price - entry_price
    trades.append({
        'entry_time': entry_time,
        'exit_time': exit_time,
        'entry_price': entry_price,
        'exit_price': exit_price,
        'pnl': pnl
    })


# 9) Print trade summary
total_trades = len(trades)
total_pnl = sum(t['pnl'] for t in trades)
wins = sum(1 for t in trades if t['pnl'] > 0)
losses = sum(1 for t in trades if t['pnl'] <= 0)
avg_pnl = (total_pnl / total_trades) if total_trades else 0


print("Trades:", total_trades, "Wins:", wins, "Losses:", losses)
print("Total PnL:", total_pnl, "Avg PnL per trade:", avg_pnl)
## -------------------------------------------------------------------

## Implementing winning rate 

no_of_winning_trades = wins
Total_trade = total_trades

win_rate = (wins/Total_trade)*100
print(f"Win Rate : {win_rate:.2f}%")

## -------------------------------------------------------------------
# --- Sharpe Ratio ---
# Daily returns from trades
returns = [t['pnl'] / t['entry_price'] for t in trades]  # percentage returns

if len(returns) > 1:
    mean_return = np.mean(returns)
    std_return = np.std(returns, ddof=1)  # sample std dev
    sharpe_ratio = (mean_return / std_return) * np.sqrt(len(returns))  # annualize by √N
else:
    sharpe_ratio = 0.0

print("Sharpe Ratio:", sharpe_ratio)

## -------------------------------------------------------------------

# 10) Plot (plot a range if too much data)
# If your dataset is very large, slice df.tail(500) or a date range to make the chart readable.
plot_df = df.tail(800)   # for example, last 800 candles
mpf.plot(plot_df,
         type='candle',
         mav=(20,50),
         volume=True,
         style='yahoo',
         addplot=[mpf.make_addplot(plot_df['buy_marker']), mpf.make_addplot(plot_df['sell_marker'])],
         title="BTC Historical with SMA(20,50) and Buy/Sell markers")


## used to plot the all dropdowns while backtesting 

## --------------------------------------------------------------------------------------------------
# apds = [
#     mpf.make_addplot(plot_df['buy_marker'], type='scatter', marker='^', markersize=60, color='g'),
#     mpf.make_addplot(plot_df['sell_marker'], type='scatter', marker='v', markersize=60, color='r'),
#     mpf.make_addplot(drawdown_series.loc[plot_df.index], panel=1, color='b', ylabel='Drawdown')
# ]

# mpf.plot(plot_df,
#          type='candle',
#          mav=(20,50),
#          volume=True,
#          style='yahoo',
#          addplot=apds,
#          title="BTC Historical with SMA(20,50), Buy/Sell markers & Drawdown")

## -----------------------------------------------------------------------------------------------

