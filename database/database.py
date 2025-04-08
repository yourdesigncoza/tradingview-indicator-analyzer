from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

    def save_indicator(self, indicator_data):
        with self.get_session() as session:
            indicator = Indicator(**indicator_data)
            session.add(indicator)
            return indicator

    def get_indicator(self, url):
        with self.get_session() as session:
            return session.query(Indicator).filter(Indicator.url == url).first()

    def get_all_indicators(self):
        with self.get_session() as session:
            return session.query(Indicator).all()

    def log_analysis(self, indicator_id, status, error_message=None, execution_time=0):
        with self.get_session() as session:
            log = AnalysisLog(
                indicator_id=indicator_id,
                status=status,
                error_message=error_message,
                execution_time=execution_time
            )
            session.add(log)