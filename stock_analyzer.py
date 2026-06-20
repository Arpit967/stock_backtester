import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class StockAnalyzer:
    def __init__(self, symbols: list):
        self.symbols = symbols
        self.data={}
        
    def fetch(self, period ="1y"):
        for symbol in self.symbols:
            df=yf.download(symbol, period=period)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            df['daily_return']=df['Close'].pct_change()
            df['SMA_20'] = df['Close'].rolling(20).mean()
            df['SMA_50'] = df['Close'].rolling(50).mean()
            df['volatility']=df['daily_return'].rolling(20).std()
            
            self.data[symbol]=df
            print(f"Fetch {symbol} -> {len(df)} days of data")
            
        return self
    
    def sharpe_ratio(self, symbol):
        df=self.data[symbol]
        annual_return=df['daily_return'].mean()*252
        annual_vol=df['volatility'].iloc[-1]*(252**0.5)
        return annual_return/annual_vol    
    
    def summary(self):
        print("\n"+"="*65)
        print(f" {'SYMBOL':15} {'PRICE':>10} {'ANN.RETURN':>10} {'SHARPE':>10}")
        print("="*65)
        for sym in self.symbols:
            df = self.data[sym]
            price = df['Close'].iloc[-1].item()
            ret = df['daily_return'].mean() * 252
            sharpe = self.sharpe_ratio(sym)
            print(f"{sym:15} ₹{price:>9.2f} {ret:>11.2%} {sharpe:>8.2f}")
        print("="*65)
        
    def plot(self, symbol):
        df = self.data[symbol]
        plt.figure(figsize=(12, 6))
        plt.plot(df['Close'], label='Price', linewidth=1)
        plt.plot(df['SMA_20'], label='SMA 20', linewidth=1.5)
        plt.plot(df['SMA_50'], label='SMA 50', linewidth=1.5)
        plt.title(f"{symbol} — Price + Moving Averages")
        plt.xlabel("Date")
        plt.ylabel("Price (₹)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{symbol}_chart.png")
        plt.show(block=True)
        print(f"Chart saved → {symbol}_chart.png")
        
if __name__ == "__main__":
    analyzer =StockAnalyzer([
        "TCS.NS",
        "INFY.NS", 
        "RELIANCE.NS",
        "HDFCBANK.NS",
        "ITC.NS"
    ])
        
    analyzer.fetch()
    analyzer.summary()
    analyzer.plot("TCS.NS")
    analyzer.plot("INFY.NS")
    analyzer.plot("RELIANCE.NS")
    analyzer.plot("HDFCBANK.NS")
    analyzer.plot("ITC.NS")