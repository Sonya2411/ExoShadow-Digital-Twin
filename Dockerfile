# Используем официальный легковесный образ Python 3.10
FROM python:3.10-slim-bookworm

# Установка системных переменных
# PYTHONDONTWRITEBYTECODE — запрещает Python создавать файлы .pyc
# PYTHONUNBUFFERED — позволяет выводить логи в реальном времени
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Установка системных зависимостей (необходимы для сборки некоторых библиотек анализа данных)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование файла зависимостей для эффективного кэширования слоев Docker
COPY requirements.txt .

# Установка Python-библиотек (FastAPI, Pandas, NumPy, Pydantic, Uvicorn)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов проекта (исходный код, модели, конфиги) в контейнер
COPY . .

# Указываем порт, который будет прослушивать приложение
EXPOSE 8000

# Команда для запуска приложения с использованием ASGI-сервера Uvicorn
# Принимаем соединения на всех интерфейсах (0.0.0.0) на порту 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]