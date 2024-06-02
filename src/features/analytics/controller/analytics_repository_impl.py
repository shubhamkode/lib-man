from dataclasses import dataclass

from src.shared import DatabaseService
from .analytics_repository import AnalyticsRepository

from src.features.analytics.model.analytics import Analytics


@dataclass
class AnalyticsRepositoryImpl(AnalyticsRepository):
    db: DatabaseService

    def get(self) -> Analytics:
        student_count = self.db.query("SELECT COUNT(*) FROM STUDENT").fetchone()[0]
        book_count = self.db.query("SELECT COUNT(*) FROM BOOK").fetchone()[0]
        borrowed_book_count = self.db.query("SELECT COUNT(*) FROM RECORD").fetchone()[0]

        return Analytics(
            student_count=student_count,
            book_count=book_count,
            borrowed_book_count=borrowed_book_count,
        )
