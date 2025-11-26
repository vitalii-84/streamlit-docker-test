# streamlit-docker-test



# 🏗️ Архітектура рішення для аналітичних застосунків 


## 🏗️ Архітектура Системи

### 📊 Загальна Схема

```
┌─────────────────────────────────────────────────────────────┐
│                    АРХІТЕКТУРА                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│    ┌──────────────┐           ┌─────────────┐              │
│    │   Browser    │  ←────→   │  Streamlit  │              │
│    │              │           │     App     │              │
│    │ localhost:   │  HTTP     │             │              │
│    │   8501       │           │   Port 8501 │              │
│    └──────────────┘           └──────┬──────┘              │
│                                       │                      │
│                                       │ SQL                  │
│                                       │ Queries              │
│                                       ▼                      │
│                              ┌─────────────┐                │
│                              │ PostgreSQL  │                │
│                              │  Database   │                │
│                              │             │                │
│                              │  Port 5432  │                │
│                              └─────────────┘                │
│                                                               │
│    Volume: postgres_data (Persistent Storage)               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Потік Даних

```mermaid
graph TB
    A[👤 Користувач] -->|HTTP запит| B[🌐 Browser<br/>localhost:8501]
    B -->|Відображення UI| A
    B <-->|HTTP Protocol<br/>GET/POST| C[📊 Streamlit App<br/>Port 8501]
    C -->|SQL Queries<br/>SELECT/INSERT/UPDATE| D[🐘 PostgreSQL<br/>Database<br/>Port 5432]
    D -->|Результати запитів<br/>Rows/Data| C
    D <-->|Читання/Запис| E[💾 Volume<br/>postgres_data<br/>Persistent Storage]
    
    style A fill:#e1f5ff
    style B fill:#fff3cd
    style C fill:#d4edda
    style D fill:#cce5ff
    style E fill:#f8d7da
```

---

## 📦 Компоненти Системи

### **1️⃣ Browser (Клієнт)**
```
┌─────────────────────┐
│     🌐 Browser      │
│                     │
│  • Chrome/Firefox   │
│  • localhost:8501   │
│  • UI відображення  │
│  • User input       │
└─────────────────────┘
```

**Функції:**
- Відображає веб-інтерфейс Streamlit
- Приймає ввід від користувача
- Відправляє HTTP запити до Streamlit App
- Отримує HTML/CSS/JavaScript відповіді

---

### **2️⃣ Streamlit App (Application Layer)**
```
┌─────────────────────┐
│  📊 Streamlit App   │
│                     │
│  • Python          │
│  • Port 8501       │
│  • Business Logic  │
│  • Data Processing │
└─────────────────────┘
```

**Функції:**
- Веб-сервер на порту 8501
- Обробка логіки застосунку
- Відправка SQL запитів до PostgreSQL
- Візуалізація даних (графіки, таблиці)
- Обробка user input

**Технологічний стек:**
- Python 3.x
- Streamlit Framework
- SQLAlchemy / psycopg2
- Pandas, NumPy
- Plotly / Matplotlib

---

### **3️⃣ PostgreSQL (Database Layer)**
```
┌─────────────────────┐
│  🐘 PostgreSQL DB   │
│                     │
│  • Version 15      │
│  • Port 5432       │
│  • SQL Engine      │
│  • Data Storage    │
└─────────────────────┘
```

**Функції:**
- Зберігання даних у таблицях
- Виконання SQL запитів
- Транзакційна цілісність
- Індексація та оптимізація
- ACID властивості

**Конфігурація:**
- User: `your_user`
- Database: `your_database`
- Password: `your_password`
- Port: `5432`

---

### **4️⃣ Volume (Storage Layer)**
```
┌─────────────────────┐
│  💾 postgres_data   │
│                     │
│  • Named Volume    │
│  • Persistent      │
│  • /var/lib/       │
│    postgresql/data │
└─────────────────────┘
```

**Функції:**
- Постійне зберігання даних БД
- Зберігається після `docker-compose down`
- Backup та відновлення
- Ізоляція від контейнера

---

## 🔌 Підключення та Порти

### **Мережеві З'єднання:**

```
Користувач
    ↓
    ↓ HTTP (port 8501)
    ↓
Streamlit Container
    ↓
    ↓ PostgreSQL Protocol (port 5432)
    ↓ Connection String:
    ↓ postgresql://your_user:your_password@postgres:5432/your_database
    ↓
PostgreSQL Container
    ↓
    ↓ File I/O
    ↓
Docker Volume (postgres_data)
```

### **Таблиця Портів:**

| Компонент    | Internal Port | External Port | Протокол | Доступ                |
|--------------|---------------|---------------|----------|-----------------------|
| Streamlit    | 8501          | 8501          | HTTP     | localhost:8501        |
| PostgreSQL   | 5432          | 5432          | TCP      | localhost:5432        |

---

## 🔐 Комунікація між Компонентами

### **1. Browser ↔ Streamlit**

```python
# HTTP Request від Browser
GET http://localhost:8501/

# Streamlit Response
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <body>
    <div id="streamlit-app">
      <!-- Streamlit UI components -->
    </div>
  </body>
</html>
```

**Протокол:** HTTP/1.1  
**Формат:** HTML, CSS, JavaScript  
**Тип:** Request/Response

---

### **2. Streamlit ↔ PostgreSQL**

```python
# Приклад з'єднання в Streamlit App
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# З'єднання через Docker network
DATABASE_URL = "postgresql://your_user:your_password@postgres:5432/your_database"
engine = create_engine(DATABASE_URL)

# SQL Query
query = "SELECT * FROM sales WHERE date > '2024-01-01'"
df = pd.read_sql(query, engine)

# Відображення в Streamlit
st.dataframe(df)
```

**Протокол:** PostgreSQL Wire Protocol (TCP)  
**Формат:** SQL Queries → Binary Result Sets  
**Тип:** Client/Server

---

### **3. PostgreSQL ↔ Volume**

```bash
# PostgreSQL пише дані
/var/lib/postgresql/data/
├── base/           # Таблиці та індекси
├── global/         # Глобальні дані
├── pg_wal/         # Write-Ahead Log
└── pg_stat_tmp/    # Статистика
```

**Протокол:** File System I/O  
**Формат:** Binary Files  
**Тип:** Read/Write Operations

---

## 🌐 Docker Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Docker Bridge Network                       │
│            (default compose network)                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│   ┌──────────────────┐         ┌──────────────────┐    │
│   │  streamlit_app   │ ◄────► │   postgres_db    │    │
│   │                  │         │                  │    │
│   │  IP: 172.18.0.2  │         │  IP: 172.18.0.3  │    │
│   │  Port: 8501      │         │  Port: 5432      │    │
│   └────────┬─────────┘         └────────┬─────────┘    │
│            │                             │              │
│            │ Internal DNS                │              │
│            │ "postgres" → 172.18.0.3     │              │
│            │                             │              │
└────────────┼─────────────────────────────┼──────────────┘
             │                             │
             │ Port Binding                │ Port Binding
             │ 8501:8501                   │ 5432:5432
             ▼                             ▼
        ┌─────────────────────────────────────────┐
        │         Host Network (localhost)        │
        │                                          │
        │  localhost:8501 → Streamlit             │
        │  localhost:5432 → PostgreSQL            │
        └─────────────────────────────────────────┘
```

---

## 📊 Діаграма Послідовності (Sequence Diagram)

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant B as 🌐 Browser
    participant S as 📊 Streamlit
    participant P as 🐘 PostgreSQL
    participant V as 💾 Volume

    U->>B: Відкриває localhost:8501
    B->>S: HTTP GET /
    S->>B: HTML/CSS/JS
    B->>U: Відображає UI
    
    U->>B: Натискає кнопку "Show Data"
    B->>S: HTTP POST /data
    
    S->>P: SQL: SELECT * FROM sales
    P->>V: Читає дані з диску
    V->>P: Повертає дані
    P->>S: Результат запиту (rows)
    
    S->>S: Обробляє дані (Pandas)
    S->>S: Створює графік (Plotly)
    S->>B: HTML з візуалізацією
    B->>U: Показує графік
```

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Security Layers                        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Layer 1: Network Isolation                              │
│  ├─ Docker Internal Network                              │
│  └─ PostgreSQL недоступний ззовні (тільки через         │
│     Streamlit)                                           │
│                                                           │
│  Layer 2: Authentication                                 │
│  ├─ PostgreSQL User/Password                            │
│  └─ Connection String в environment variables            │
│                                                           │
│  Layer 3: Data Persistence                               │
│  ├─ Volume з обмеженим доступом                         │
│  └─ Backup можливості                                    │
│                                                           │
│  Layer 4: Container Isolation                            │
│  ├─ Окремі файлові системи                              │
│  └─ Resource limits (CPU/Memory)                         │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Flow

```
┌─────────────────────────────────────────────────────────┐
│              Deployment Process                          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  1. docker-compose up -d                                 │
│     │                                                     │
│     ├─► Create Docker Network                            │
│     │                                                     │
│     ├─► Create Volume: postgres_data                     │
│     │                                                     │
│     ├─► Pull/Build Images                                │
│     │   ├─ postgres:15                                   │
│     │   └─ Build Streamlit from Dockerfile               │
│     │                                                     │
│     ├─► Start PostgreSQL Container                       │
│     │   ├─ Initialize Database                           │
│     │   ├─ Create User                                    │
│     │   ├─ Create Database                                │
│     │   └─ Health Check (pg_isready)                     │
│     │                                                     │
│     └─► Start Streamlit Container                        │
│         ├─ Wait for PostgreSQL (depends_on)              │
│         ├─ Connect to Database                            │
│         └─ Start App on port 8501                         │
│                                                           │
│  2. System Ready ✅                                      │
│     └─ Access: http://localhost:8501                     │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📈 Scalability Considerations

```
Current Architecture:
┌─────────────────┐
│   1 Streamlit   │
│   1 PostgreSQL  │
└─────────────────┘

Future Scaling:
┌─────────────────────────────────────┐
│  Load Balancer (NGINX)              │
├─────────────────────────────────────┤
│  Streamlit 1  │  Streamlit 2  │ ... │
├─────────────────────────────────────┤
│  PostgreSQL Primary                  │
│  PostgreSQL Replicas (Read-only)    │
├─────────────────────────────────────┤
│  Redis Cache                         │
└─────────────────────────────────────┘
```

---

## 💾 Data Flow Diagram

```
User Input → Browser → Streamlit → PostgreSQL → Volume
                ↓         ↓           ↓           ↓
            Display ← Processing ← Query ← Data Storage
```

---

## ✅ Summary

| Компонент      | Роль                  | Технологія    | Port  |
|----------------|-----------------------|---------------|-------|
| **Browser**    | User Interface        | HTML/CSS/JS   | 8501  |
| **Streamlit**  | Application Logic     | Python        | 8501  |
| **PostgreSQL** | Data Storage          | SQL Database  | 5432  |
| **Volume**     | Persistent Storage    | Docker Volume | N/A   |

**Архітектура:** 3-tier (Presentation → Application → Data)  
**Комунікація:** HTTP + PostgreSQL Protocol  
**Оркестрація:** Docker Compose  
**Зберігання:** Docker Named Volume

---



### Cкрипт комплексної перевірки

```bash
chmod +x check_all.sh
./check_all.sh

```


## Варіант 1: 

### 1.1 Встановіть необхідні утиліти (curl)

```bash

apt-get update && apt-get install -y procps curl netcat-openbsd

```

### 1.2 Перевірте, чи Streamlit відповідає

```bash
curl http://localhost:8501

# Перевірте статус
curl -I http://localhost:8501

```

## Варіант 2: Використайте Python (curl не потрібен)

```bash
python3 << EOF
import urllib.request
try:
    response = urllib.request.urlopen('http://localhost:8501')
    print(f"✅ Streamlit працює! Status: {response.status}")
except Exception as e:
    print(f"❌ Streamlit не відповідає: {e}")
EOF
```




```python
# Запустіть тест
python test_db.py
```


## Варіант 3: Перевірте процес Streamlit

```bash
# Перевірте, чи Streamlit запущено
ps aux | grep streamlit

nc -zv localhost 8501
```

## Варіант 4: Запустіть Streamlit (якщо не запущено)

```bash
# Перевірте, чи існує app.py
ls -la app.py

# Запустіть Streamlit
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Ви маєте побачити:

```
  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501
```

## Варіант 5: Відкрийте в браузері (найпростіше)

1. У VS Code знизу відкрийте вкладку **"PORTS"**
2. Знайдіть порт **8501**
3. Клікніть на іконку **🌐** (Open in Browser)

Це найнадійніший спосіб!

## Варіант 6: Перевірте з хост-терміналу

Відкрийте **новий локальний термінал** у VS Code:

1. Натисніть `F1`
2. Виберіть: **"Terminal: Create New Terminal (Local)"**
3. У новому терміналі:

```bash
# Перевірте контейнер Streamlit
docker compose ps

# Перегляньте логи
docker compose logs streamlit

# Або
docker logs streamlit_app
```

## Швидкий тест Python

```bash
python3 -c "
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 8501))
if result == 0:
    print('✅ Порт 8501 відкритий - Streamlit працює!')
else:
    print('❌ Порт 8501 закритий - Streamlit не запущено')
sock.close()
"
```

## Якщо Streamlit не запущено, запустіть його:

```bash
# У фоновому режимі
nohup streamlit run app.py --server.address 0.0.0.0 > streamlit.log 2>&1 &

# Перегляньте лог
tail -f streamlit.log
```

Найкращий спосіб — просто відкрийте порт 8501 через вкладку **PORTS** у VS Code! 🎯





-------------------------------------------------------------------------------------------------------


У вашому контейнері немає багатьох утиліт. Використайте Python для перевірки:

## Варіант 1: Перевірте через Python

```bash
python3 << 'EOF'
import socket

# Перевірка порту 8501
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('localhost', 8501))
if result == 0:
    print('✅ Порт 8501 ВІДКРИТИЙ - Streamlit працює!')
else:
    print('❌ Порт 8501 ЗАКРИТИЙ - Streamlit НЕ запущено')
sock.close()

# Перевірка порту 5432 (PostgreSQL)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result2 = sock2.connect_ex(('postgres', 5432))
if result2 == 0:
    print('✅ Порт 5432 ВІДКРИТИЙ - PostgreSQL працює!')
else:
    print('❌ Порт 5432 ЗАКРИТИЙ - PostgreSQL НЕ працює')
sock2.close()
EOF
```

## Варіант 2: Просто запустіть Streamlit

```bash
# Перевірте, чи є файл app.py
ls -la app.py

# Запустіть Streamlit
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Якщо побачите це — все працює:
```
  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501
```

## Варіант 3: Відкрийте PORTS у VS Code

**Це найпростіший спосіб:**

1. У VS Code знизу знайдіть вкладку **"PORTS"** (біля Terminal, Problems, Debug Console)
2. Побачите список портів:
   ```
   8501 - streamlit
   5432 - postgres
   ```
3. Клікніть на іконку **🌐** біля порту 8501
4. Streamlit відкриється в браузері!

## Варіант 4: Встановіть необхідні утиліти (якщо потрібно)

```bash
apt-get update && apt-get install -y procps curl netcat-openbsd

# Тепер можете використовувати:
ps aux | grep streamlit
curl http://localhost:8501
nc -zv localhost 8501
```

## Варіант 5: Перевірте з нового терміналу (на хості)

У VS Code:
1. Натисніть `Ctrl + Shift + P` (або `F1`)
2. Введіть: **"Terminal: Create New Terminal (Local)"**
3. У новому терміналі (це буде хост, НЕ контейнер):

```bash
# Перевірте контейнери
docker compose ps

# Логи Streamlit
docker compose logs streamlit

# Логи PostgreSQL
docker compose logs postgres

# Перевірте порти
docker compose ps | grep -E "8501|5432"
```

## Варіант 6: Тест підключення до PostgreSQL

```bash
python3 << 'EOF'
import psycopg2

try:
    conn = psycopg2.connect(
        host="postgres",
        database="your_database",
        user="your_user",
        password="your_password",
        connect_timeout=3
    )
    print("✅ PostgreSQL підключення УСПІШНЕ!")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(f"Версія: {cur.fetchone()[0][:50]}...")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ PostgreSQL помилка: {e}")
EOF
```

## Варіант 7: Комплексна перевірка

```bash
python3 << 'EOF'
import os
import socket
import sys

print("=" * 50)
print("🔍 ДІАГНОСТИКА СЕРЕДОВИЩА")
print("=" * 50)

# 1. Поточна директорія
print(f"\n📂 Директорія: {os.getcwd()}")

# 2. Файли
print(f"\n📁 Файли:")
for f in os.listdir('.'):
    print(f"  - {f}")

# 3. Python версія
print(f"\n🐍 Python: {sys.version.split()[0]}")

# 4. Встановлені пакети
print(f"\n📦 Пакети:")
try:
    import streamlit
    print(f"  ✅ streamlit: {streamlit.__version__}")
except:
    print(f"  ❌ streamlit: не встановлено")

try:
    import psycopg2
    print(f"  ✅ psycopg2: {psycopg2.__version__}")
except:
    print(f"  ❌ psycopg2: не встановлено")

try:
    import pandas as pd
    print(f"  ✅ pandas: {pd.__version__}")
except:
    print(f"  ❌ pandas: не встановлено")

# 5. Порт 8501
print(f"\n🌐 Порт 8501 (Streamlit):")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock.connect_ex(('localhost', 8501)) == 0:
    print(f"  ✅ ВІДКРИТИЙ")
else:
    print(f"  ❌ ЗАКРИТИЙ (запустіть Streamlit!)")
sock.close()

# 6. Порт 5432
print(f"\n🐘 Порт 5432 (PostgreSQL):")
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock2.connect_ex(('postgres', 5432)) == 0:
    print(f"  ✅ ДОСТУПНИЙ")
else:
    print(f"  ❌ НЕДОСТУПНИЙ")
sock2.close()

print("\n" + "=" * 50)
print("✅ Діагностика завершена!")
print("=" * 50)
EOF
```

## Рекомендація:

**Найпростіше — використайте вкладку PORTS у VS Code!** Вона покаже всі доступні порти і дозволить відкрити Streamlit одним кліком. 🎯

Якщо хочете запустити Streamlit вручну:

```bash
streamlit run app.py --server.address 0.0.0.0
```







