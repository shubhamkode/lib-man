from abc import ABC, abstractmethod

from src.features.analytics.model.analytics import Analytics


class AnalyticsRepository(ABC):
    @abstractmethod
    def get(self) -> Analytics:
        pass
