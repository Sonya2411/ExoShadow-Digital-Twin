# services/analytics_service.py
import pandas as pd
from typing import List
from models import TelemetryFrame

class AnalyticsService:
    @staticmethod
    def aggregate_statistics(frames: List[TelemetryFrame]):
        if not frames:
            return {}

        data = []
        for f in frames:
            data.append({
                "timestamp": f.timestamp,
                "pwr": f.battery_voltage * sum(s.current for s in f.servos),
                "l_knee": f.servos[1].angle,
                "r_knee": f.servos[3].angle,
                "max_t": max(s.temperature for s in f.servos)
            })
        
        df = pd.DataFrame(data)
        
        stats = {
            "avg_power_watt": float(df["pwr"].mean()),
            "critical_temp": float(df["max_t"].max()),
            "rom": {
                "l_knee": float(df["l_knee"].max() - df["l_knee"].min()),
                "r_knee": float(df["r_knee"].max() - df["r_knee"].min())
            }
        }
        return stats