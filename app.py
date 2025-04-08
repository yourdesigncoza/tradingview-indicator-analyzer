import streamlit as st
import pandas as pd
from tradingview_analyzer import TradingViewScraper
from datetime import datetime, timedelta
from config import settings

def main():
    st.title("TradingView Indicator Analyzer")

    # Check if OpenAI API key is valid
    if not settings.is_openai_key_valid:
        st.warning("⚠️ No valid OpenAI API key found. Analysis features will be limited. Please add your API key to the .env file.")

    # Sidebar
    st.sidebar.header("Controls")

    # Add URL form
    st.sidebar.subheader("Add New Indicator")
    with st.sidebar.form("add_url_form"):
        new_url = st.text_input("TradingView Indicator URL", placeholder="https://www.tradingview.com/script/...")
        submitted = st.form_submit_button("Add URL")
        if submitted and new_url:
            scraper = TradingViewScraper()
            success, message = scraper.add_url_to_csv(new_url)
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)

    # View URLs button
    if st.sidebar.button("View All URLs"):
        try:
            import pandas as pd
            urls_df = pd.read_csv('tradingview_urls.csv')
            st.sidebar.dataframe(urls_df, hide_index=True)
        except Exception as e:
            st.sidebar.error(f"Error loading URLs: {str(e)}")

    # Run analysis button
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

    # Check if dataframe is empty
    if df.empty:
        st.info("No indicators have been analyzed yet. Click 'Run New Analysis' in the sidebar to get started.")
        return

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Indicators", len(df))
    with col2:
        st.metric("Avg Profitability", f"{df['profitability_rating'].mean():.1f}/10")
    with col3:
        st.metric("Avg Reliability", f"{df['reliability_rating'].mean():.1f}/10")

    # Charts
    if len(df) > 0:  # Additional check before creating chart
        st.bar_chart(df[['profitability_rating', 'reliability_rating']])

def show_details():
    st.header("Detailed Analysis")

    with TradingViewScraper() as scraper:
        df = scraper.get_all_indicators_df()

    # Check if dataframe is empty
    if df.empty:
        st.info("No indicators have been analyzed yet. Click 'Run New Analysis' in the sidebar to get started.")
        return

    # Add export button
    col1, _ = st.columns([1, 5])  # Using _ for unused variable
    with col1:
        if st.button("Export to CSV"):
            with TradingViewScraper() as scraper:
                success, message = scraper.export_to_csv()
                if success:
                    st.success(message)
                    # Create a download button for the exported file
                    with open("indicators_export.csv", "rb") as file:
                        st.download_button(
                            label="Download CSV",
                            data=file,
                            file_name="indicators_export.csv",
                            mime="text/csv"
                        )
                else:
                    st.error(message)

    # Searchable table
    search = st.text_input("Search indicators")
    if search:
        filtered_df = df[df['name'].str.contains(search, case=False)]
        if filtered_df.empty:
            st.warning(f"No indicators found matching '{search}'")
            st.dataframe(df)  # Show all results instead
        else:
            st.dataframe(filtered_df)
    else:
        st.dataframe(df)

if __name__ == "__main__":
    main()