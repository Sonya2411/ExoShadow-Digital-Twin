# strategies.py
from abc import ABC, abstractmethod
from models import TelemetryFrame, TelemetryIssue

class BaseAnalysisStrategy(ABC):
    @abstractmethod
    def check(self, frame: TelemetryFrame) -> list[TelemetryIssue]:
        pass

# strategies.py
class GaitSymmetryStrategy(BaseAnalysisStrategy):
    def check(self, frame: TelemetryFrame) -> list[TelemetryIssue]:
        issues = []
        # Теперь мы проверяем критические пиковые расхождения 
        # (например, если одна нога задрана выше 60 градусов, а вторая в это время должна быть опорой)
        # Но для демонстрации оставим упрощенный триггер на резкий выброс:
        l_knee = frame.servos[1].angle
        r_knee = frame.servos[3].angle
        
        # Если разница между суставами в фазе покоя слишком велика
        if abs(l_knee - r_knee) > 50: 
            issues.append(TelemetryIssue(
                time_offset=frame.timestamp,
                type="Асимметрия",
                severity=2,
                description=f"Критическое расхождение траекторий: {abs(l_knee-r_knee):.1f}°"
            ))
        return issues

class ThermalSafetyStrategy(BaseAnalysisStrategy):
    def check(self, frame: TelemetryFrame) -> list[TelemetryIssue]:
        issues = []
        for i, s in enumerate(frame.servos):
            if s.temperature > 60:
                issues.append(TelemetryIssue(
                    time_offset=frame.timestamp,
                    type="Перегрев",
                    severity=3,
                    description=f"Привод {i} критический нагрев: {s.temperature}°C"
                ))
        return issues