import openai
import logging
from typing import Dict, Any
from datetime import datetime
from config import settings

class IndicatorAnalyzer:
    def __init__(self, api_key: str = None):
        # Use the provided api_key or default to the one in settings
        self.api_key = api_key or settings.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo-16k"  # or "gpt-4" depending on needs

    async def analyze_indicator(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Check if we're using a dummy API key (for testing)
            if self.api_key == 'sk-dummy-key-for-testing':
                logging.warning("Using dummy OpenAI API key. Returning mock analysis.")
                return self._generate_mock_analysis(data)

            prompt = self._create_analysis_prompt(data)
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a trading indicator analysis expert."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the response into structured format
            analysis = self._parse_gpt_response(response.choices[0].message.content)
            return analysis
        except Exception as e:
            logging.error(f"Analysis failed for {data['name']}: {str(e)}")
            raise

    def _generate_mock_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock analysis for testing purposes"""
        return {
            'url': data.get('url', 'https://example.com'),
            'name': data.get('name', 'Mock Indicator'),
            'functionality': "This is a mock analysis for testing purposes.",
            'usage_guidelines': "These are mock usage guidelines.",
            'user_feedback': "This is mock user feedback.",
            'additional_insights': "These are mock additional insights.",
            'profitability_rating': 5,  # Middle rating for mock
            'reliability_rating': 5,     # Middle rating for mock
            'analyzed_date': datetime.now()
        }

    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
        Please analyze and summarize this indicator '{data['name']}' from TradingView.

        Description: {data['description']}

        User Comments: {' '.join(data['comments'][:10])}  # Limiting to first 10 comments

        Please provide analysis in the following JSON structure:
        {{
            "indicator_functionality": "",
            "usage_guidelines": "",
            "user_feedback": {{"positive": [], "negative": []}},
            "additional_insights": "",
            "ratings": {{"profitability": 0-10, "reliability": 0-10}}
        }}
        """

    def _parse_gpt_response(self, response: str) -> Dict[str, Any]:
        """Parse the GPT response into a structured format

        In a real implementation, this would parse JSON from the response.
        For now, we'll return a simple mock structure.
        """
        # This is a simplified implementation
        # In a real scenario, you would parse the JSON from the response
        try:
            # Just using the response string to show it's being used
            logging.info(f"Parsing response of length: {len(response)}")

            # Return a mock structure for now
            return {
                'functionality': "Extracted from response...",
                'usage_guidelines': "Extracted from response...",
                'user_feedback': "Extracted from response...",
                'additional_insights': "Extracted from response...",
                'profitability_rating': 7,
                'reliability_rating': 8,
                'analyzed_date': datetime.now()
            }
        except Exception as e:
            logging.error(f"Error parsing GPT response: {str(e)}")
            raise