# 示例用 yfinance（后续可换成 SEC / AlphaVantage / FinancialModelingPrep 等 API）

import yfinance as yf


def get_price_data(ticker, period="1y"):
    """获取单只或列表标的的价格数据。"""
    data = yf.download(ticker, period=period, progress=False, group_by="ticker", auto_adjust=True)
    return data


def get_macro_data(symbol="^TNX"):
    """获取宏观数据（如 10Y 国债利率）。"""
    data = yf.download(symbol, period="1y", progress=False, auto_adjust=True)
    return data
