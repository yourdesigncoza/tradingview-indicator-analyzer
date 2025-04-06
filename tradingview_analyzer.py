import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime
import csv
import os
from config import settings

class TradingViewScraper:
    def __init__(self, db_path=None):
        # Use the provided db_path or default to the one in settings
        self.db_path = db_path or os.path.join(settings.DATA_DIR, "indicators.db")
        self.setup_database()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS indicators (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    name TEXT,
                    description TEXT,
                    functionality TEXT,
                    usage_guidelines TEXT,
                    user_feedback TEXT,
                    additional_insights TEXT,
                    profitability_rating INTEGER,
                    reliability_rating INTEGER,
                    analyzed_date TIMESTAMP
                )
            """)

    def scrape_indicator(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract relevant data
            name = soup.find('h1', {'class': 'title'}).text.strip()
            description = soup.find('div', {'class': 'description'}).text.strip()
            comments = soup.find_all('div', {'class': 'comment'})

            # Compile data for analysis
            data = {
                'name': name,
                'description': description,
                'comments': [c.text.strip() for c in comments],
                'url': url
            }
            return data
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def process_urls_from_csv(self, csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                url = row[0]
                data = self.scrape_indicator(url)
                if data:
                    analysis = self.analyze_indicator(data)
                    self.save_to_db(analysis)

    def analyze_indicator(self, data):
        # Here you would implement the analysis based on your prompt template
        # This is a placeholder structure
        analysis = {
            'url': data['url'],
            'name': data['name'],
            'functionality': "Analysis of how it works...",
            'usage_guidelines': "Usage guidelines analysis...",
            'user_feedback': "User feedback analysis...",
            'additional_insights': "Additional insights...",
            'profitability_rating': 7,  # Example rating
            'reliability_rating': 8,     # Example rating
            'analyzed_date': datetime.now()
        }
        return analysis

    def save_to_db(self, analysis):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO indicators
                (url, name, functionality, usage_guidelines, user_feedback,
                additional_insights, profitability_rating, reliability_rating, analyzed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis['url'], analysis['name'], analysis['functionality'],
                analysis['usage_guidelines'], analysis['user_feedback'],
                analysis['additional_insights'], analysis['profitability_rating'],
                analysis['reliability_rating'], analysis['analyzed_date']
            ))

    def get_all_indicators_df(self):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM indicators"
            df = pd.read_sql_query(query, conn)
            return df

def main():
    scraper = TradingViewScraper()
    scraper.process_urls_from_csv('tradingview_urls.csv')

if __name__ == "__main__":
    main()