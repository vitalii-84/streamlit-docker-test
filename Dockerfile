FROM python:3.11-slim

WORKDIR /app

# Встановіть залежності системи
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Скопіюйте файл залежностей
COPY requirements.txt .

# Встановіть Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Скопіюйте код додатку
COPY . .

# Відкрийте порт Streamlit
EXPOSE 8501

# Запустіть Streamlit
# CMD ["streamlit", "run", "app_test.py", "--server.address", "0.0.0.0"]
CMD ["streamlit", "run", "bike-store-dashboard.py", "--server.address", "0.0.0.0"]

