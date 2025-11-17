import csv
import pandas as pd
from datetime import datetime

class OrderEngine:
    def __init__(self, fund=10000, file="pnl_log.csv"):
        self.fund = fund
        self.position = False
        self.entry_price = None
        self.logfile = file

        with open(self.logfile, "w") as f:
            f.write("time,action,price,pnl,fund\n")

    def process(self, entry_signal, exit_signal, price):
        if price is None:
            return "NO_PRICE"

        if entry_signal and not self.position:
            self.position = True
            self.entry_price = price
            self._log("BUY", price, pnl=0)
            return "BUY"

        if exit_signal and self.position:
            pnl = price - self.entry_price
            self.fund += pnl
            self.position = False
            self._log("SELL", price, pnl)
            return "SELL"

        return "HOLD"

    def _log(self, action, price, pnl):
        with open(self.logfile, "a") as f:
            f.write(f"{datetime.now()},{action},{price},{pnl},{self.fund}\n")



        df = pd.read_csv(self.logfile)
        df.to_excel("pnl_log.xlsx", index=False)
