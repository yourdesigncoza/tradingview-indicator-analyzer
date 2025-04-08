from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Indicator(Base):
    __tablename__ = 'indicators'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    functionality = Column(String)
    usage_guidelines = Column(String)
    user_feedback = Column(JSON)
    additional_insights = Column(String)
    profitability_rating = Column(Float)
    reliability_rating = Column(Float)
    raw_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalysisLog(Base):
    __tablename__ = 'analysis_logs'

    id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer)
    status = Column(String)
    error_message = Column(String, nullable=True)
    execution_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)