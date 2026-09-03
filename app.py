import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Импортируем ваши классы и сервисы
from models import TelemetryUpload
from engine import ShadowEngine
from strategies import GaitSymmetryStrategy, ThermalSafetyStrategy
from services.analytics_service import AnalyticsService

# 1. Создаем приложение (ОПРЕДЕЛЯЕМ 'app' ПЕРВЫМ)
app = FastAPI(title="ExoShadow Digital Twin")

# 2. Инициализируем движок анализа
engine = ShadowEngine(strategies=[
    GaitSymmetryStrategy(),
    ThermalSafetyStrategy()
])

# 3. Настраиваем папку для интерфейса (статические файлы)
if not os.path.exists("static"):
    os.makedirs("static")

# Монтируем статику, чтобы сервер видел index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- МАРШРУТЫ (ROUTES) ---

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Отдает главную страницу интерфейса"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Файл index.html не найден в папке static/</h1>"

@app.post("/analyze/summary")
async def get_summary(payload: TelemetryUpload):
    """Принимает данные, анализирует и возвращает отчет"""
    try:
        # Анализ на аномалии (ShadowEngine)
        anomalies = engine.process_session(payload.data)
        
        # Расчет статистики (Pandas Service)
        stats = AnalyticsService.aggregate_statistics(payload.data)
        
        # Формируем итоговый JSON-отчет
        report = {
            "session_id": payload.session_id,
            "statistics": stats,
            "anomalies_found": len(anomalies),
            "anomalies": [iss.model_dump() for iss in anomalies]
        }
        
        # Сохраняем историю в файл (Репозиторий)
        with open("reports_history.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")
            
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)