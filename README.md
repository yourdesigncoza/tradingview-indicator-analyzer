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