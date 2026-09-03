from models import TelemetryFrame, TelemetryIssue

class ShadowEngine:
    def __init__(self, strategies: list):
        self.strategies = strategies

    def process_session(self, frames: list[TelemetryFrame]) -> list[TelemetryIssue]:
        all_issues = []
        for frame in frames:
            for strategy in self.strategies:
                all_issues.extend(strategy.check(frame))
        return all_issues