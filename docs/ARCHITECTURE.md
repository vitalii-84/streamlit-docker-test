Я створю декілька варіантів графічної візуалізації цієї архітектури для вас.

## 🎨 Графічна Візуалізація Архітектури

### **Варіант 1: Mermaid - Вертикальна Архітектура**

```mermaid
graph TB
    subgraph Client["🖥️ Client Layer"]
        Browser["🌐 Browser<br/>localhost:8501"]
    end
    
    subgraph Application["📦 Application Container"]
        Streamlit["📊 Streamlit App<br/>Port: 8501<br/>Python Framework"]
    end
    
    subgraph Database["📦 Database Container"]
        PostgreSQL["🐘 PostgreSQL 15<br/>Port: 5432<br/>Relational Database"]
    end
    
    subgraph Storage["💾 Storage Layer"]
        Volume["💿 Docker Volume<br/>postgres_data<br/>Persistent Storage"]
    end
    
    Browser <-->|"HTTP Protocol<br/>GET/POST"| Streamlit
    Streamlit <-->|"SQL Queries<br/>SELECT/INSERT/UPDATE"| PostgreSQL
    PostgreSQL <-->|"File I/O<br/>Read/Write"| Volume
    
    style Browser fill:#fff3cd,stroke:#856404,stroke-width:3px
    style Streamlit fill:#d4edda,stroke:#155724,stroke-width:3px
    style PostgreSQL fill:#cce5ff,stroke:#004085,stroke-width:3px
    style Volume fill:#f8d7da,stroke:#721c24,stroke-width:3px
```

---

### **Варіант 2: Mermaid - Горизонтальний Flow**

```mermaid
flowchart LR
    A["🌐<br/>Browser<br/><br/>localhost:8501"]
    B["📊<br/>Streamlit<br/>App<br/>Port 8501"]
    C["🐘<br/>PostgreSQL<br/>Database<br/>Port 5432"]
    D["💾<br/>Volume<br/><br/>postgres_data"]
    
    A <-->|HTTP| B
    B <-->|SQL| C
    C <-->|I/O| D
    
    style A fill:#fff9c4,stroke:#f57f17,stroke-width:4px,color:#000
    style B fill:#c8e6c9,stroke:#388e3c,stroke-width:4px,color:#000
    style C fill:#bbdefb,stroke:#1976d2,stroke-width:4px,color:#000
    style D fill:#ffccbc,stroke:#d84315,stroke-width:4px,color:#000
```

---

### **Варіант 3: Детальна Архітектура з Docker**

```mermaid
graph TB
    subgraph External["🌍 External World"]
        User["👤 User"]
    end
    
    subgraph Host["💻 Host Machine - localhost"]
        Browser["🌐 Web Browser<br/>Access: http://localhost:8501"]
        
        subgraph Docker["🐳 Docker Environment"]
            
            subgraph Network["🔌 Docker Bridge Network"]
                
                subgraph Container1["📦 streamlit_app Container"]
                    App["📊 Streamlit Application<br/>━━━━━━━━━━━━━━━━━<br/>• Python 3.x<br/>• Pandas & Plotly<br/>• SQLAlchemy<br/>━━━━━━━━━━━━━━━━━<br/>Port: 8501"]
                end
                
                subgraph Container2["📦 postgres_db Container"]
                    DB["🐘 PostgreSQL 15<br/>━━━━━━━━━━━━━━━━━<br/>• POSTGRES_USER<br/>• POSTGRES_PASSWORD<br/>• POSTGRES_DB<br/>━━━━━━━━━━━━━━━━━<br/>Port: 5432"]
                end
                
            end
            
            Vol["💾 Docker Volume<br/>━━━━━━━━━━━━━━━━━<br/>Name: postgres_data<br/>Path: /var/lib/postgresql/data<br/>Type: Persistent Storage"]
        end
    end
    
    User -->|"Opens"| Browser
    Browser <-->|"HTTP Protocol<br/>Request/Response"| App
    App <-->|"PostgreSQL Protocol<br/>SQL Queries"| DB
    DB <-->|"File System I/O<br/>Data Persistence"| Vol
    
    style User fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style Browser fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style App fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
    style DB fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style Vol fill:#ffccbc,stroke:#bf360c,stroke-width:3px
    style Docker fill:#f5f5f5,stroke:#616161,stroke-width:2px,stroke-dasharray: 5 5
    style Network fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,stroke-dasharray: 5 5
```

---

### **Варіант 4: Sequence Diagram (Послідовність Взаємодії)**

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Browser as 🌐 Browser<br/>(localhost:8501)
    participant Streamlit as 📊 Streamlit<br/>(Port 8501)
    participant PostgreSQL as 🐘 PostgreSQL<br/>(Port 5432)
    participant Volume as 💾 Volume<br/>(postgres_data)
    
    User->>Browser: 1. Opens localhost:8501
    Browser->>Streamlit: 2. HTTP GET /
    Streamlit-->>Browser: 3. Returns HTML/CSS/JS
    Browser-->>User: 4. Displays UI
    
    User->>Browser: 5. User Action (e.g., "Load Data")
    Browser->>Streamlit: 6. HTTP POST Request
    
    Streamlit->>PostgreSQL: 7. SQL Query<br/>(SELECT * FROM table)
    PostgreSQL->>Volume: 8. Read Data from Disk
    Volume-->>PostgreSQL: 9. Return Data
    PostgreSQL-->>Streamlit: 10. Query Results (Rows)
    
    Streamlit->>Streamlit: 11. Process Data<br/>(Pandas/NumPy)
    Streamlit->>Streamlit: 12. Generate Visualization<br/>(Plotly/Matplotlib)
    Streamlit-->>Browser: 13. Return Updated HTML
    Browser-->>User: 14. Display Results
    
    Note over Volume: ⚡ Data persists even after<br/>docker-compose down
```

---

### **Варіант 5: Компонентна Діаграма з Layers**

```mermaid
graph TB
    subgraph L1["🎨 Presentation Layer"]
        P1["🌐 Web Browser<br/>━━━━━━━━━━━━━━<br/>• HTML/CSS/JS<br/>• User Interface<br/>• localhost:8501"]
    end
    
    subgraph L2["⚙️ Application Layer - Docker Container"]
        A1["📊 Streamlit Framework<br/>Business Logic & UI"]
        A2["🐍 Python Runtime<br/>Data Processing Engine"]
        A3["📈 Visualization Libraries<br/>Plotly, Matplotlib, Seaborn"]
    end
    
    subgraph L3["💾 Data Layer - Docker Container"]
        D1["🐘 PostgreSQL Engine<br/>SQL Query Processor"]
        D2["📊 Database Schemas<br/>Tables, Indexes, Relations"]
    end
    
    subgraph L4["💿 Storage Layer - Docker Volume"]
        S1["📁 File System<br/>postgres_data<br/>/var/lib/postgresql/data"]
    end
    
    P1 <-->|HTTP/WebSocket| A1
    A1 <--> A2
    A2 <--> A3
    A2 <-->|SQL Commands| D1
    D1 <--> D2
    D2 <-->|I/O Operations| S1
    
    style L1 fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style L2 fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    style L3 fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style L4 fill:#ffccbc,stroke:#d84315,stroke-width:3px
```

---

### **Варіант 6: Network Topology**

```mermaid
graph TB
    subgraph HostNet["🖥️ Host Network (localhost)"]
        Port8501[":8501 ⚡"]
        Port5432[":5432 ⚡"]
    end
    
    subgraph DockerNet["🐳 Docker Bridge Network<br/>subnet: 172.18.0.0/16"]
        
        subgraph SC["📦 Streamlit Container<br/>IP: 172.18.0.2"]
            SA["📊 Streamlit App<br/>Internal Port: 8501"]
        end
        
        subgraph PC["📦 PostgreSQL Container<br/>IP: 172.18.0.3"]
            PA["🐘 PostgreSQL DB<br/>Internal Port: 5432"]
        end
        
        DNS["🔍 Internal DNS<br/>━━━━━━━━━━━━━━<br/>postgres → 172.18.0.3<br/>streamlit → 172.18.0.2"]
    end
    
    Port8501 -.Port Binding.-> SA
    Port5432 -.Port Binding.-> PA
    
    SA -->|"Connection String:<br/>postgresql://user:pass@postgres:5432/db"| PA
    
    DNS -.Name Resolution.-> SA
    DNS -.Name Resolution.-> PA
    
    style Port8501 fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style Port5432 fill:#fff9c4,stroke:#f57f17,stroke-width:3px
    style SA fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    style PA fill:#bbdefb,stroke:#1565c0,stroke-width:3px
    style DNS fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    style DockerNet fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,stroke-dasharray: 5 5
```

---

### **Варіант 7: Data Flow Diagram**

```mermaid
flowchart TD
    Start([👤 User Opens Browser])
    
    Start --> B1[🌐 Browser sends HTTP GET<br/>to localhost:8501]
    B1 --> S1[📊 Streamlit receives request]
    S1 --> S2{Need Data<br/>from DB?}
    
    S2 -->|Yes| D1[🐘 PostgreSQL: Execute SQL Query]
    D1 --> D2[💾 Volume: Read data from disk]
    D2 --> D3[📊 Return query results]
    D3 --> S3[🐍 Process data with Pandas]
    
    S2 -->|No| S3
    
    S3 --> S4[📈 Create visualization<br/>Plotly/Matplotlib]
    S4 --> S5[🎨 Generate HTML response]
    S5 --> B2[🌐 Browser renders page]
    B2 --> End([👤 User sees dashboard])
    
    style Start fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    style B1 fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style S1 fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style S2 fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style D1 fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style D2 fill:#ffccbc,stroke:#bf360c,stroke-width:2px
    style End fill:#e1f5fe,stroke:#01579b,stroke-width:3px
```

---

### **Варіант 8: Deployment View**

```mermaid
graph LR
    subgraph Compose["📄 docker-compose.yml"]
        YML["version: '3.8'<br/>━━━━━━━━━━━━<br/>services:<br/>• postgres<br/>• streamlit<br/>━━━━━━━━━━━━<br/>volumes:<br/>• postgres_data"]
    end
    
    YML -->|defines| Srv1[Service:<br/>postgres]
    YML -->|defines| Srv2[Service:<br/>streamlit]
    YML -->|defines| Vol[Volume:<br/>postgres_data]
    
    Srv1 -->|creates| C1["📦 Container<br/>postgres_db<br/>━━━━━━━━━━<br/>Image: postgres:15<br/>Port: 5432"]
    Srv2 -->|creates| C2["📦 Container<br/>streamlit_app<br/>━━━━━━━━━━<br/>Build: Dockerfile<br/>Port: 8501"]
    
    C1 -->|mounts| Vol
    C2 -->|depends_on| C1
    
    C1 -->|exposes| P1["🔌 Port 5432"]
    C2 -->|exposes| P2["🔌 Port 8501"]
    
    P2 -->|accessible at| URL["🌐 http://localhost:8501"]
    
    style YML fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style C1 fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style C2 fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    style Vol fill:#ffccbc,stroke:#bf360c,stroke-width:2px
    style URL fill:#fff9c4,stroke:#f57f17,stroke-width:3px
```

---

### **Варіант 9: Technology Stack**

```mermaid
mindmap
  root((🐳 Docker<br/>Compose<br/>Stack))
    🌐 Frontend
      Browser
        Chrome
        Firefox
        Safari
      Protocol
        HTTP/1.1
        WebSocket
      Port
        8501
    📊 Application
      Streamlit
        Python 3.x
        Web Framework
        Auto-reload
      Libraries
        Pandas
        NumPy
        Plotly
        Matplotlib
        SQLAlchemy
    🐘 Database
      PostgreSQL 15
        SQL Engine
        ACID Compliant
        Relational DB
      Features
        Transactions
        Indexes
        Foreign Keys
        JSON Support
    💾 Storage
      Docker Volume
        Named Volume
        Persistent
        postgres_data
      Location
        /var/lib/postgresql/data
```

---

### **Варіант 10: Простий Icon Flow**

```mermaid
flowchart LR
    A["👤"]
    B["💻"]
    C["📊"]
    D["🐘"]
    E["💾"]
    
    A -->|User| B
    B -->|Browser<br/>:8501| C
    C -->|Streamlit<br/>App| D
    D -->|PostgreSQL<br/>:5432| E
    E -->|Volume<br/>postgres_data| E
    
    style A fill:#e3f2fd,stroke:#1976d2,stroke-width:4px
    style B fill:#fff9c4,stroke:#f57f17,stroke-width:4px
    style C fill:#c8e6c9,stroke:#388e3c,stroke-width:4px
    style D fill:#bbdefb,stroke:#1565c0,stroke-width:4px
    style E fill:#ffccbc,stroke:#d84315,stroke-width:4px
```

---

### **Варіант 11: ASCII Art (для документації)**

```
                    ╔══════════════════════════════════════════╗
                    ║     🐳 Docker Compose Architecture       ║
                    ╚══════════════════════════════════════════╝

                              👤 User
                               │
                               │ Opens browser
                               ▼
                    ┌─────────────────────────┐
                    │   🌐 Web Browser         │
                    │   localhost:8501         │
                    └────────────┬─────────────┘
                                 │
                                 │ HTTP GET/POST
                                 ▼
        ╔═══════════════════════════════════════════════════════════╗
        ║              🐳 DOCKER ENVIRONMENT                         ║
        ║                                                            ║
        ║   ┌─────────────────────────────────────────────────┐    ║
        ║   │  📦 Streamlit Container (streamlit_app)          │    ║
        ║   │  ┌────────────────────────────────────────────┐ │    ║
        ║   │  │  📊 Streamlit Application                   │ │    ║
        ║   │  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ │    ║
        ║   │  │  • Framework: Streamlit                    │ │    ║
        ║   │  │  • Language: Python 3.x                    │ │    ║
        ║   │  │  • Libraries: Pandas, Plotly               │ │    ║
        ║   │  │  • Port: 8501                              │ │    ║
        ║   │  └────────────────┬───────────────────────────┘ │    ║
        ║   └───────────────────┼───────────────────────────────┘    ║
        ║                       │                                     ║
        ║                       │ SQL Queries                         ║
        ║                       │ (SELECT, INSERT, UPDATE, DELETE)    ║
        ║                       ▼                                     ║
        ║   ┌─────────────────────────────────────────────────┐    ║
        ║   │  📦 PostgreSQL Container (postgres_db)           │    ║
        ║   │  ┌────────────────────────────────────────────┐ │    ║
        ║   │  │  🐘 PostgreSQL 15 Database                  │ │    ║
        ║   │  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │ │    ║
        ║   │  │  • POSTGRES_USER: your_user                │ │    ║
        ║   │  │  • POSTGRES_DB: your_database              │ │    ║
        ║   │  │  • Port: 5432                              │ │    ║
        ║   │  └────────────────┬───────────────────────────┘ │    ║
        ║   └───────────────────┼───────────────────────────────┘    ║
        ║                       │                                     ║
        ║                       │ File I/O (Read/Write)              ║
        ║                       ▼                                     ║
        ║   ┌─────────────────────────────────────────────────┐    ║
        ║   │  💾 Docker Named Volume                          │    ║
        ║   │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    ║
        ║   │  Name: postgres_data                             │    ║
        ║   │  Mount: /var/lib/postgresql/data                │    ║
        ║   │  Type: Persistent Storage                        │    ║
        ║   │  ⚡ Survives: docker-compose down                │    ║
        ║   └─────────────────────────────────────────────────┘    ║
        ╚═══════════════════════════════════════════════════════════╝

                        Legend:
                        ━━━━━━━━━━━━━━━━━━━
                        📦  Docker Container
                        💾  Docker Volume
                        🌐  Web Browser
                        📊  Application
                        🐘  Database
                        👤  User
```

---

### **Варіант 12: State Diagram (Життєвий Цикл)**

```mermaid
stateDiagram-v2
    [*] --> Stopped: Initial State
    
    Stopped --> Creating: docker-compose up -d
    
    Creating --> PostgreSQLStarting: Create containers
    PostgreSQLStarting --> HealthChecking: Start PostgreSQL
    
    HealthChecking --> Healthy: pg_isready ✓
    HealthChecking --> HealthChecking: Retry every 10s
    HealthChecking --> Failed: Max retries (5)
    
    Healthy --> StreamlitStarting: depends_on satisfied
    StreamlitStarting --> Running: App initialization complete
    
    Running --> Running: Handle HTTP requests
    Running --> Paused: docker-compose pause
    Paused --> Running: docker-compose unpause
    
    Running --> Stopping: docker-compose stop
    Stopping --> Stopped
    
    Stopped --> [*]: docker-compose down -v
    Failed --> [*]: Error state
    
    note right of HealthChecking
        Health Check Config:
        • Test: pg_isready -U your_user
        • Interval: 10s
        • Timeout: 5s
        • Retries: 5
    end note
    
    note right of Running
        Active State:
        • Browser ⟷ Streamlit (HTTP)
        • Streamlit ⟷ PostgreSQL (SQL)
        • Volume persists data
    end note
```

---

## 📊 Порівняльна Таблиця

```mermaid
graph LR
    subgraph "Component Comparison"
        A[Browser<br/>UI Layer]
        B[Streamlit<br/>App Layer]
        C[PostgreSQL<br/>Data Layer]
        D[Volume<br/>Storage Layer]
    end
    
    style A fill:#fff9c4,stroke:#f57f17
    style B fill:#c8e6c9,stroke:#388e3c
    style C fill:#bbdefb,stroke:#1565c0
    style D fill:#ffccbc,stroke:#d84315
```

| Layer | Component | Technology | Port | Purpose |
|-------|-----------|------------|------|---------|
| 🎨 Presentation | Browser | HTML/CSS/JS | 8501 | User Interface |
| ⚙️ Application | Streamlit | Python 3.x | 8501 | Business Logic |
| 💾 Data | PostgreSQL | SQL Database | 5432 | Data Storage |
| 💿 Storage | Volume | File System | N/A | Persistence |

---

**Всі ці діаграми можна використовувати в:**
- 📄 Документації (Markdown)
- 🎓 Презентаціях (PowerPoint/Google Slides)  
- 📚 Wiki (Confluence/Notion)
- 💻 GitHub/GitLab README
- 🎨 Архітектурних документах

**Mermaid автоматично рендериться на більшості сучасних платформ!** ✨🚀📊
