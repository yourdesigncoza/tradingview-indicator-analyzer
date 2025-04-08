from sqlalchemy import or_, and_, func
from .models import Indicator, AnalysisLog
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class IndicatorQueries:
    def __init__(self, db_session):
        self.session = db_session

    def search_indicators(
        self,
        query: str = None,
        min_profitability: float = None,
        min_reliability: float = None,
        date_from: datetime = None,
        date_to: datetime = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Indicator]:
        """
        Advanced search functionality for indicators
        """
        filters = []
        
        if query:
            filters.append(
                or_(
                    Indicator.name.ilike(f'%{query}%'),
                    Indicator.description.ilike(f'%{query}%'),
                    Indicator.functionality.ilike(f'%{query}%')
                )
            )
            
        if min_profitability:
            filters.append(Indicator.profitability_rating >= min_profitability)
            
        if min_reliability:
            filters.append(Indicator.reliability_rating >= min_reliability)
            
        if date_from:
            filters.append(Indicator.created_at >= date_from)
            
        if date_to:
            filters.append(Indicator.created_at <= date_to)

        return self.session.query(Indicator)\
            .filter(and_(*filters))\
            .order_by(Indicator.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_statistics(self) -> Dict:
        """
        Get general statistics about indicators
        """
        return {
            'total_indicators': self.session.query(func.count(Indicator.id)).scalar(),
            'avg_profitability': self.session.query(func.avg(Indicator.profitability_rating)).scalar(),
            'avg_reliability': self.session.query(func.avg(Indicator.reliability_rating)).scalar(),
            'recent_additions': self.session.query(func.count(Indicator.id))\
                .filter(Indicator.created_at >= datetime.now() - timedelta(days=7))\
                .scalar()
        }

    def get_top_indicators(self, limit: int = 10) -> List[Indicator]:
        """
        Get top performing indicators based on combined ratings
        """
        return self.session.query(Indicator)\
            .order_by((Indicator.profitability_rating + Indicator.reliability_rating).desc())\
            .limit(limit)\
            .all()

    def get_analysis_history(self, indicator_id: int) -> List[AnalysisLog]:
        """
        Get analysis history for a specific indicator
        """
        return self.session.query(AnalysisLog)\
            .filter(AnalysisLog.indicator_id == indicator_id)\
            .order_by(AnalysisLog.created_at.desc())\
            .all()

    def get_similar_indicators(self, indicator_id: int, limit: int = 5) -> List[Indicator]:
        """
        Find similar indicators based on name and description
        """
        indicator = self.session.query(Indicator).get(indicator_id)
        if not indicator:
            return []
            
        return self.session.query(Indicator)\
            .filter(Indicator.id != indicator_id)\
            .order_by(
                func.similarity(Indicator.name, indicator.name) +
                func.similarity(Indicator.description, indicator.description)
            ).limit(limit).all()