# 🐳 Dockerfile - Повне Пояснення

## 📋 Що таке Dockerfile?

**Dockerfile** - це текстовий файл з інструкціями для автоматичного створення Docker образу (image).

### **Проста Аналогія:**

```
📖 Dockerfile = Рецепт для Приготування Страви

Кулінарний рецепт:
1. Візьміть основу (тісто)
2. Додайте інгредієнти (овочі, м'ясо)
3. Встановіть температуру (180°C)
4. Запікайте 30 хвилин
5. Подавайте на стіл

Dockerfile:
1. Візьміть базовий образ (FROM python:3.11)
2. Додайте файли проекту (COPY . /app)
3. Встановіть залежності (RUN pip install)
4. Відкрийте порт (EXPOSE 8501)
5. Запустіть застосунок (CMD ["python", "app.py"])

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Dockerfile → docker build → Docker Image → docker run → Container
  (рецепт)   (приготування)   (готова страва) (подача)   (тарілка)
```

---

## 🎯 Навіщо потрібен Dockerfile?

### **Без Dockerfile (Проблема):**

```bash
# Вам треба пояснити колезі як запустити проект:

1. Встанови Python 3.11
2. Створи папку /app
3. Скопіюй всі файли
4. pip install pandas==2.0.0
5. pip install streamlit==1.28.0
6. pip install psycopg2-binary==2.9.7
7. pip install sqlalchemy==2.0.20
8. Встанови системні пакети: gcc, postgresql-dev
9. Налаштуй змінні оточення
10. Запусти: streamlit run app.py

❌ Складно!
❌ Можуть бути помилки
❌ "Works on my machine" problem
❌ Різні версії на різних машинах
```

### **З Dockerfile (Рішення):**

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
# Одна команда для всіх!
docker build -t my-app .
docker run -p 8501:8501 my-app

✅ Просто!
✅ Працює однаково скрізь
✅ Автоматизовано
✅ Версіоновано (в Git)
```

---

## 📖 Основні Інструкції Dockerfile

### **1. FROM - Базовий Образ**

```dockerfile
# Вибрати базовий образ
FROM python:3.11-slim

# Інші приклади:
FROM node:18-alpine          # Node.js (мінімальний)
FROM ubuntu:22.04            # Ubuntu Linux
FROM postgres:15             # PostgreSQL
FROM nginx:alpine            # NGINX web server
FROM scratch                 # Порожній образ (мінімум)
```

**Що це:**
- Вихідна точка для вашого образу
- Базова операційна система + інструменти
- Завантажується з Docker Hub

---

### **2. WORKDIR - Робоча Директорія**

```dockerfile
# Встановити робочу директорію
WORKDIR /app

# Всі наступні команди виконуються в /app
# Якщо папки немає - створюється автоматично
```

**Що це:**
- Встановлює поточну директорію всередині контейнера
- Як `cd /app` але постійно

---

### **3. COPY - Копіювати Файли**

```dockerfile
# Копіювати з host → container
COPY source destination

# Приклади:
COPY app.py /app/               # Один файл
COPY . /app                     # Вся поточна папка
COPY requirements.txt .         # В WORKDIR
COPY ./data /app/data           # Папка з вмістом
```

**Що це:**
- Копіює файли з вашого комп'ютера в образ
- Працює тільки під час `docker build`

---

### **4. ADD - Розширене Копіювання**

```dockerfile
# Схоже на COPY, але з додатковими можливостями
ADD archive.tar.gz /app/        # Розпакує автоматично
ADD https://example.com/file.txt /app/  # Завантажить з URL

# ⚠️ Рекомендація: використовуйте COPY, якщо не потрібні особливі функції ADD
```

---

### **5. RUN - Виконати Команду**

```dockerfile
# Виконати команду під час побудови образу
RUN command

# Приклади:
RUN pip install pandas
RUN apt-get update && apt-get install -y gcc
RUN npm install
RUN mkdir /app/logs

# Об'єднання команд (зменшує розмір образу)
RUN apt-get update && \
    apt-get install -y \
        gcc \
        postgresql-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*
```

**Що це:**
- Виконується під час `docker build`
- Кожен RUN створює новий layer (шар) в образі
- Результат зберігається в образі

---

### **6. CMD - Команда За Замовчуванням**

```dockerfile
# Команда, яка виконується при запуску контейнера
CMD ["executable", "param1", "param2"]

# Приклади:
CMD ["python", "app.py"]
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
CMD ["npm", "start"]

# Shell форма (не рекомендована):
CMD python app.py
```

**Що це:**
- Виконується при `docker run`
- Може бути тільки один CMD
- Можна перевизначити: `docker run my-image python other.py`

---

### **7. ENTRYPOINT - Точка Входу**

```dockerfile
# Основна команда контейнера
ENTRYPOINT ["executable"]

# Приклад:
ENTRYPOINT ["python"]
CMD ["app.py"]  # Аргумент за замовчуванням

# Запуск:
docker run my-image              # python app.py
docker run my-image test.py      # python test.py
```

**Різниця CMD vs ENTRYPOINT:**
- CMD - можна повністю замінити
- ENTRYPOINT - базова команда (додаються аргументи)

---

### **8. EXPOSE - Відкрити Порт**

```dockerfile
# Документує який порт використовує застосунок
EXPOSE 8501

# Приклади:
EXPOSE 80           # HTTP
EXPOSE 443          # HTTPS
EXPOSE 5432         # PostgreSQL
EXPOSE 3000         # API

# Не робить порт доступним! Це тільки документація
# Для доступу потрібно: docker run -p 8501:8501
```

---

### **9. ENV - Змінні Оточення**

```dockerfile
# Встановити змінні оточення
ENV KEY=value

# Приклади:
ENV NODE_ENV=production
ENV DATABASE_URL=postgresql://localhost/mydb
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/bin:${PATH}"

# Багато змінних:
ENV NODE_ENV=production \
    PORT=3000 \
    DEBUG=false
```

**Що це:**
- Змінні доступні всередині контейнера
- Можна перевизначити: `docker run -e PORT=5000`

---

### **10. ARG - Аргументи Побудови**

```dockerfile
# Змінні тільки під час docker build
ARG VERSION=3.11
ARG PYTHON_VERSION

FROM python:${VERSION}-slim

# Використання:
docker build --build-arg VERSION=3.10 -t my-app .
```

**Різниця ARG vs ENV:**
- ARG - тільки під час `docker build`
- ENV - під час `docker build` + `docker run`

---

### **11. VOLUME - Точка Монтування**

```dockerfile
# Оголосити volume
VOLUME /data
VOLUME ["/app/logs", "/app/cache"]

# Створює точку монтування для persistent data
```

---

### **12. USER - Користувач**

```dockerfile
# Змінити користувача (security best practice)
RUN useradd -m appuser
USER appuser

# За замовчуванням все виконується як root (небезпечно!)
```

---

### **13. HEALTHCHECK - Перевірка Здоров'я**

```dockerfile
# Перевірка чи застосунок працює
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8501/ || exit 1

# Або для Python:
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8501')"
```

---

### **14. LABEL - Метадані**

```dockerfile
# Додати метадані до образу
LABEL version="1.0"
LABEL maintainer="vitalii@example.com"
LABEL description="Streamlit Analytics Dashboard"
```

---

## 📦 Повний Приклад: Streamlit App

### **Dockerfile для Streamlit + PostgreSQL**

```dockerfile
# ============================================
# Multi-stage Dockerfile для Streamlit App
# ============================================

# ────────────────────────────────────────────
# Stage 1: Builder (для встановлення залежностей)
# ────────────────────────────────────────────
FROM python:3.11-slim AS builder

# Встановити системні залежності для компіляції
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Створити робочу директорію
WORKDIR /app

# Копіювати requirements.txt
COPY requirements.txt .

# Встановити Python залежності
RUN pip install --no-cache-dir --user -r requirements.txt

# ────────────────────────────────────────────
# Stage 2: Runtime (фінальний образ)
# ────────────────────────────────────────────
FROM python:3.11-slim

# Metadata
LABEL maintainer="vitalii@khartiia.io"
LABEL version="1.0"
LABEL description="Streamlit Analytics Dashboard"

# Встановити тільки runtime залежності
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Створити non-root користувача (security)
RUN useradd -m -u 1000 streamlit && \
    mkdir -p /app && \
    chown -R streamlit:streamlit /app

# Змінити на non-root користувача
USER streamlit

# Встановити робочу директорію
WORKDIR /app

# Копіювати встановлені пакети з builder stage
COPY --from=builder --chown=streamlit:streamlit /root/.local /home/streamlit/.local

# Додати Python packages до PATH
ENV PATH=/home/streamlit/.local/bin:$PATH

# Змінні оточення
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Копіювати код застосунку
COPY --chown=streamlit:streamlit . .

# Відкрити порт Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Запустити Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **requirements.txt**

```txt
streamlit==1.28.0
pandas==2.1.0
plotly==5.17.0
psycopg2-binary==2.9.7
sqlalchemy==2.0.20
numpy==1.25.2
```

### **app.py (простий приклад)**

```python
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

st.title('📊 Analytics Dashboard')

# З'єднання з БД
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@postgres:5432/db')

try:
    engine = create_engine(DATABASE_URL)
    
    # Завантажити дані
    df = pd.read_sql('SELECT * FROM sales LIMIT 100', engine)
    
    st.dataframe(df)
    st.bar_chart(df.groupby('region')['amount'].sum())
    
except Exception as e:
    st.error(f'Error connecting to database: {e}')
```

---

## 🏗️ Побудова та Запуск

### **Команди:**

```bash
# 1. Побудувати образ
docker build -t streamlit-app:1.0 .

# З аргументами
docker build \
  --build-arg PYTHON_VERSION=3.11 \
  --tag streamlit-app:1.0 \
  --file Dockerfile \
  .

# 2. Переглянути створений образ
docker images

# 3. Запустити контейнер
docker run -d \
  --name my-streamlit \
  -p 8501:8501 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/mydb \
  streamlit-app:1.0

# 4. Переглянути логи
docker logs -f my-streamlit

# 5. Зупинити
docker stop my-streamlit

# 6. Видалити
docker rm my-streamlit
```

---

## 🎯 Best Practices для Dockerfile

### **1. Використовуйте .dockerignore**

```bash
# .dockerignore (як .gitignore для Docker)
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
.vscode/
.idea/
*.md
.env
.DS_Store
node_modules/
*.log
```

### **2. Multi-stage Builds (зменшення розміру)**

```dockerfile
# Поганий спосіб (великий образ):
FROM python:3.11
RUN apt-get install gcc g++ ... (багато залежностей)
COPY . .
RUN pip install -r requirements.txt
# Фінальний образ: 1.5 GB ❌

# Гарний спосіб (малий образ):
FROM python:3.11 AS builder
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
# Фінальний образ: 500 MB ✅
```

### **3. Мінімізуйте Layers**

```dockerfile
# Погано (багато layers):
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
RUN apt-get clean

# Добре (один layer):
RUN apt-get update && \
    apt-get install -y package1 package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### **4. Оптимізуйте Порядок (Cache)**

```dockerfile
# Погано (кеш постійно інвалідується):
COPY . /app                    # Весь код
RUN pip install -r requirements.txt

# Добре (використовує кеш):
COPY requirements.txt .        # Тільки залежності
RUN pip install -r requirements.txt
COPY . /app                    # Код (змінюється частіше)
```

### **5. Security Best Practices**

```dockerfile
# 1. Не використовуйте root
USER appuser

# 2. Не зберігайте секрети в образі
# Погано:
ENV DB_PASSWORD=secret123  ❌

# Добре:
# Передавайте через docker run -e або secrets
docker run -e DB_PASSWORD=secret123  ✅

# 3. Оновлюйте базові образи
FROM python:3.11-slim  # Регулярно оновлюйте

# 4. Скануйте на вразливості
docker scan my-image
```

### **6. Використовуйте Specific Versions**

```dockerfile
# Погано:
FROM python:latest         ❌
RUN pip install pandas     ❌

# Добре:
FROM python:3.11.5-slim   ✅
RUN pip install pandas==2.1.0  ✅
```

---

## 🔄 Життєвий Цикл Docker Image

```
┌─────────────────────────────────────────────────────────────┐
│                   DOCKER IMAGE LIFECYCLE                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Написати Dockerfile                                      │
│     │                                                         │
│     ▼                                                         │
│  2. docker build -t my-app:1.0 .                            │
│     │                                                         │
│     ├─► Читає Dockerfile                                    │
│     ├─► Виконує кожну інструкцію                           │
│     ├─► Створює layers (шари)                              │
│     ├─► Кешує результати                                    │
│     │                                                         │
│     ▼                                                         │
│  3. Docker Image (готовий шаблон)                           │
│     │                                                         │
│     ├─► docker images (переглянути)                         │
│     ├─► docker tag (позначити версію)                       │
│     ├─► docker push (завантажити на Docker Hub)            │
│     │                                                         │
│     ▼                                                         │
│  4. docker run my-app:1.0                                    │
│     │                                                         │
│     ├─► Створює Container з Image                           │
│     ├─► Виконує CMD/ENTRYPOINT                              │
│     │                                                         │
│     ▼                                                         │
│  5. Running Container (працюючий застосунок)                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Dockerfile vs docker-compose.yml

| Аспект | Dockerfile | docker-compose.yml |
|--------|-----------|-------------------|
| **Призначення** | Створення одного образу | Оркестрація багатьох контейнерів |
| **Що описує** | Як побудувати образ | Як запустити сервіси |
| **Команда** | `docker build` | `docker-compose up` |
| **Формат** | Dockerfile DSL | YAML |
| **Використання** | Один застосунок | Багато застосунків разом |
| **Приклад** | Python app образ | App + DB + Redis |

---


## ✅ Підсумок

```yaml
═══════════════════════════════════════════════════════════════════════
                        DOCKERFILE - ГОЛОВНЕ
═══════════════════════════════════════════════════════════════════════

Що це:
  📄 Текстовий файл з інструкціями для побудови Docker образу
  🔨 "Рецепт" для створення контейнера
  📦 Автоматизація створення середовища

Основні інструкції:
  FROM:        Базовий образ
  WORKDIR:     Робоча директорія
  COPY:        Копіювати файли
  RUN:         Виконати команду (build time)
  CMD:         Команда за замовчуванням (run time)
  EXPOSE:      Документувати порт
  ENV:         Змінні оточення

Best Practices:
  ✅ Multi-stage builds (зменшення розміру)
  ✅ .dockerignore (виключення файлів)
  ✅ Specific versions (не latest)
  ✅ Minimal layers (об'єднання RUN)
  ✅ Non-root user (security)
  ✅ Health checks (моніторинг)

Переваги:
  ✅ Відтворюваність (працює скрізь однаково)
  ✅ Версіонування (зберігається в Git)
  ✅ Автоматизація (CI/CD)
  ✅ Ізоляція (кожен образ незалежний)


```

**Dockerfile - це інструкція як "спакувати" ваш застосунок у портативний, відтворюваний контейнер!** 🐳📦🚀🇺🇦
