import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from stocknews import StockNews

# Initialize session state variables
if 'ticker' not in st.session_state:
    st.session_state.ticker = []
if 'data' not in st.session_state:
    st.session_state.data = {}

# App title
st.title('💰STOCK Dashboard')

# Sidebar: Add or remove stock tickers
st.sidebar.title('Stock Ticker Options')
ticker_input = st.sidebar.text_input('Enter a stock ticker')
start_date = st.sidebar.date_input('Start date', pd.to_datetime('today') - pd.DateOffset(years=1))
end_date = st.sidebar.date_input('End date', pd.to_datetime('today'))

# Functions to manipulate tickers
# @st.cache_data
def add_ticker():
    if ticker_input:
        with st.spinner('Loading data...'):
            st.session_state.data[ticker_input] = yf.download(ticker_input, start=start_date, end=end_date)
            if ticker_input not in st.session_state.ticker:
                st.session_state.ticker.append(ticker_input)
        st.sidebar.write('Added:', ticker_input)
    else:
        st.sidebar.warning('Please enter a ticker.')

# @st.cache_data
def remove_ticker(ticker_to_remove):
    if ticker_to_remove in st.session_state.ticker:
        st.session_state.ticker.remove(ticker_to_remove)
        st.session_state.data.pop(ticker_to_remove)
        st.sidebar.write('Removed:', ticker_to_remove)
    else:
        st.sidebar.warning('Ticker not found.')

@st.cache_data(experimental_allow_widgets=True) 
def display_stock_data(ticker):
    if ticker in st.session_state.data:
        df = st.session_state.data[ticker]
        df['% Change'] = df['Adj Close'].pct_change().fillna(0)
        fig = px.line(df, x=df.index, y='Adj Close', title=f'{ticker} Adjusted Close Over Time')
        st.plotly_chart(fig)
        display_custom_plot(df)

# @st.cache_data(experimental_allow_widgets=True) 
def display_custom_plot(df):
    st.header(f'Custom Data Plot for {selected_ticker}')
    df1 = df.reset_index()
    x_axis = st.selectbox('X-axis', df1.columns, index=0)
    y_axis = st.multiselect('Y-axis', df1.columns, default='Adj Close')
    plot_type = st.radio('Plot Type', ['Line', 'Scatter'])

    if plot_type == 'Line':
        fig = px.line(df1, x=x_axis, y=y_axis, title=f'{selected_ticker} Line Plot')
    else:
        fig = px.scatter(df1, x=x_axis, y=y_axis, title=f'{selected_ticker} Scatter Plot')
    st.plotly_chart(fig)

# @st.cache_data(experimental_allow_widgets=True) 
def display_stock_news(ticker):
    st.header(f'Top News for {ticker}')
    with st.spinner('Loading news...'):
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()

        for i in range(min(len(df_news), 10)):
            st.subheader(f"News {i+1}: {df_news['title'][i]}")
            st.write(df_news['published'][i])
            st.write(df_news['summary'][i])
            title_sentiment = df_news['sentiment_title'][i]
            summary_sentiment = df_news['sentiment_summary'][i]
            st.write(f"Title Sentiment: {title_sentiment}, Summary Sentiment: {summary_sentiment}")
            st.write('---')

# Sidebar buttons for adding or removing tickers
st.sidebar.button('Add Ticker', on_click=add_ticker)
if st.session_state.ticker:
    remove_target = st.sidebar.selectbox('Remove a ticker', st.session_state.ticker)
    st.sidebar.button('Remove Ticker', on_click=remove_ticker, args=(remove_target,))

# Main content: Display stock data and news
if st.session_state.ticker:
    selected_ticker = st.selectbox('Select a ticker to view', st.session_state.ticker)
    display_stock_data(selected_ticker)
    display_stock_news(selected_ticker)
else:
    st.write('Please add a ticker to display data.')