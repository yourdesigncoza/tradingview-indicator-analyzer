import pytest
from scraper.analyzer import IndicatorAnalyzer
from unittest.mock import Mock, patch

@pytest.fixture
def analyzer():
    return IndicatorAnalyzer(api_key="test_key")

def test_create_analysis_prompt():
    analyzer = IndicatorAnalyzer(api_key="test_key")
    data = {
        "name": "Test Indicator",
        "description": "Test Description",
        "comments": ["Good indicator", "Works well"]
    }
    prompt = analyzer._create_analysis_prompt(data)
    assert "Test Indicator" in prompt
    assert "Test Description" in prompt

@pytest.mark.asyncio
async def test_analyze_indicator():
    with patch('openai.ChatCompletion.acreate') as mock_create:
        mock_create.return_value.choices = [
            Mock(message=Mock(content='{"indicator_functionality": "test"}'))
        ]
        
        analyzer = IndicatorAnalyzer(api_key="test_key")
        result = await analyzer.analyze_indicator({
            "name": "Test",
            "description": "Test",
            "comments": []
        })
        
        assert isinstance(result, dict)