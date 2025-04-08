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
        # More realistic headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tradingview.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        # Add a random delay to avoid rate limiting (between 1 and 3 seconds)
        import random
        import time
        delay = random.uniform(1, 3)
        time.sleep(delay)

        try:
            # Make the request
            response = requests.get(url, headers=headers, timeout=10)

            # Check if the request was successful
            if response.status_code != 200:
                print(f"Error scraping {url}: HTTP status code {response.status_code}")
                return None

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract relevant data with better error handling
            try:
                name_element = soup.find('h1', {'class': 'title'})
                name = name_element.text.strip() if name_element else "Unknown Indicator"
            except Exception as e:
                print(f"Error extracting name from {url}: {str(e)}")
                name = "Unknown Indicator"

            try:
                description_element = soup.find('div', {'class': 'description'})
                description = description_element.text.strip() if description_element else "No description available"
            except Exception as e:
                print(f"Error extracting description from {url}: {str(e)}")
                description = "No description available"

            try:
                comments = soup.find_all('div', {'class': 'comment'})
                comment_texts = [c.text.strip() for c in comments] if comments else []
            except Exception as e:
                print(f"Error extracting comments from {url}: {str(e)}")
                comment_texts = []

            # Compile data for analysis
            data = {
                'name': name,
                'description': description,
                'comments': comment_texts,
                'url': url
            }

            print(f"Successfully scraped: {name}")
            return data

        except requests.exceptions.Timeout:
            print(f"Timeout error scraping {url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Connection error scraping {url}")
            return None
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

    def add_url_to_csv(self, url, csv_path='tradingview_urls.csv'):
        """Add a new URL to the CSV file if it doesn't already exist"""
        # Check if the URL is valid
        if not url.startswith('https://www.tradingview.com/script/'):
            return False, "URL must be a TradingView script URL (https://www.tradingview.com/script/...)"

        # Check if the file exists
        if not os.path.exists(csv_path):
            # Create the file with a header
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['url'])

        # Check if the URL already exists in the file
        existing_urls = []
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                existing_urls.append(row[0])

        if url in existing_urls:
            return False, "This URL already exists in the list"

        # Add the URL to the file
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([url])

        return True, "URL added successfully"

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

    def export_to_csv(self, output_path="indicators_export.csv"):
        """Export all indicators to a CSV file"""
        try:
            df = self.get_all_indicators_df()
            if df.empty:
                return False, "No indicators to export"

            # Format the date column
            if 'analyzed_date' in df.columns:
                df['analyzed_date'] = pd.to_datetime(df['analyzed_date']).dt.strftime('%Y-%m-%d %H:%M:%S')

            # Export to CSV
            df.to_csv(output_path, index=False)
            return True, f"Successfully exported {len(df)} indicators to {output_path}"
        except Exception as e:
            return False, f"Error exporting indicators: {str(e)}"

def main():
    scraper = TradingViewScraper()
    scraper.process_urls_from_csv('tradingview_urls.csv')

if __name__ == "__main__":
    main()