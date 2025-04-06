import streamlit as st
import pandas as pd
from scraper.tradingview_scraper import TradingViewScraper
from datetime import datetime, timedelta

def main():
    st.title("TradingView Indicator Analyzer")
    
    # Sidebar
    st.sidebar.header("Controls")
    if st.sidebar.button("Run New Analysis"):
        with st.spinner("Analyzing indicators..."):
            scraper = TradingViewScraper()
            scraper.process_urls_from_csv('tradingview_urls.csv')
    
    # Main content
    tab1, tab2 = st.tabs(["Dashboard", "Details"])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_details()

def show_dashboard():
    st.header("Analysis Dashboard")
    
    # Get data from database
    with TradingViewScraper() as scraper:
        df = scraper.get_all_indicators_df()
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Indicators", len(df))
    with col2:
        st.metric("Avg Profitability", f"{df['profitability_rating'].mean():.1f}/10")
    with col3:
        st.metric("Avg Reliability", f"{df['reliability_rating'].mean():.1f}/10")
    
    # Charts
    st.bar_chart(df[['profitability_rating', 'reliability_rating']])

def show_details():
    st.header("Detailed Analysis")
    
    with TradingViewScraper() as scraper:
        df = scraper.get_all_indicators_df()
    
    # Searchable table
    search = st.text_input("Search indicators")
    if search:
        df = df[df['name'].str.contains(search, case=False)]
    
    st.dataframe(df)

if __name__ == "__main__":
    main()