#!/bin/bash

echo "🔍 Перевірка середовища..."
echo "================================"

echo "📂 Поточна директорія:"
pwd

echo ""
echo "📁 Файли:"
ls -la

echo ""
echo "🐍 Python версія:"
python --version

echo ""
echo "📦 Встановлені пакети:"
pip list | grep -E "streamlit|psycopg2|sqlalchemy|pandas"

echo ""
echo "🐘 PostgreSQL підключення:"
psql -h postgres -U your_user -d your_database -c "SELECT version();" 2>&1

echo ""
echo "🌐 Порти:"
netstat -tuln | grep -E "8501|5432" || ss -tuln | grep -E "8501|5432"

echo ""
echo "✅ Перевірка завершена!"
EOF
