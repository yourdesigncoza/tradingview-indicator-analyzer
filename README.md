# TradingView Indicator Analyzer

An automated tool for analyzing TradingView indicators using AI-powered insights.

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd tradingview-indicator-analyzer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your credentials and configuration
   - **Important**: You must provide a valid OpenAI API key in the `.env` file. Get your API key from [OpenAI's platform](https://platform.openai.com/api-keys).

   The application uses `python-dotenv` to load environment variables from the `.env` file. The following variables are supported:

   ```
   # Required
   OPENAI_API_KEY=your_openai_api_key_here

   # Optional
   ENVIRONMENT=development  # or production
   REQUESTS_PER_MINUTE=20   # Rate limiting for API calls

   # TradingView credentials (optional)
   TRADINGVIEW_USERNAME=your_username_here
   TRADINGVIEW_PASSWORD=your_password_here

   # Database configuration (optional)
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Run the application:
```bash
streamlit run app.py
```

## Features

- Automated indicator analysis using OpenAI GPT
- Rate-limited TradingView scraping
- Interactive Streamlit dashboard
- Comprehensive error logging
- Data validation and cleaning

## Project Structure

```
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── scraper/              # Scraping modules
│   ├── __init__.py
│   ├── analyzer.py       # OpenAI analysis logic
│   ├── rate_limiter.py   # Rate limiting utilities
│   └── data_validator.py # Data validation
├── logs/                 # Log files
├── data/                 # Stored data
└── tests/                # Test files
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

MIT