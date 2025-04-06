from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional
from datetime import datetime

class IndicatorData(BaseModel):
    url: HttpUrl
    name: str
    description: str
    comments: List[str]
    
    @validator('description')
    def clean_description(cls, v):
        return ' '.join(v.split())  # Remove extra whitespace

class AnalysisResult(BaseModel):
    url: HttpUrl
    name: str
    functionality: str
    usage_guidelines: str
    user_feedback: dict
    additional_insights: str
    profitability_rating: int
    reliability_rating: int
    analyzed_date: datetime

    @validator('profitability_rating', 'reliability_rating')
    def validate_rating(cls, v):
        if not 0 <= v <= 10:
            raise ValueError('Rating must be between 0 and 10')
        return v