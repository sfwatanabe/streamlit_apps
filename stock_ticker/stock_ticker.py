"""
Simple stock price app using streamlit library.
"""

import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# Simple Stock Price App

Showing **closing price** and ***volume*** of Google!

""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

# define ticker symbol
ticker_symbol = 'AAPL'

# get data on the ticker
ticker_data = yf.Ticker(ticker_symbol)

# get historical prices for this ticker
ticker_df = ticker_data.history(period='1d', start='2010-5-31', end='2020-5-31')

st.write("""
## Closing Price
""")
st.line_chart(ticker_df.Close)
st.write("""
## Volume
""")
st.line_chart(ticker_df.Volume)