import psycopg2

def check_database_schema_simple():
    """
    Спрощена перевірка схеми бази даних PostgreSQL
    """
    try:
        # Підключення
        conn = psycopg2.connect(
            host="postgres",
            database="your_database",
            user="your_user",
            password="your_password",
            connect_timeout=5
        )
        
        cur = conn.cursor()
        
        print("=" * 80)
        print("🔍 ПЕРЕВІРКА СХЕМИ БАЗИ ДАНИХ")
        print("=" * 80)
        
        # 1. Загальна інформація
        print("\n📊 1. ЗАГАЛЬНА ІНФОРМАЦІЯ")
        print("-" * 80)
        
        cur.execute("""
            SELECT 
                current_database(),
                current_user,
                pg_size_pretty(pg_database_size(current_database()))
        """)
        
        db_info = cur.fetchone()
        print(f"База даних:  {db_info[0]}")
        print(f"Користувач:  {db_info[1]}")
        print(f"Розмір БД:   {db_info[2]}")
        
        # 2. Список таблиць
        print("\n📋 2. ТАБЛИЦІ")
        print("-" * 80)
        
        cur.execute("""
            SELECT 
                table_schema,
                table_name,
                table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
        
        tables = cur.fetchall()
        
        if tables:
            print(f"\nЗнайдено таблиць: {len(tables)}\n")
            print(f"{'Схема':<20} {'Таблиця':<30} {'Тип':<15}")
            print("-" * 65)
            for table in tables:
                print(f"{table[0]:<20} {table[1]:<30} {table[2]:<15}")
        else:
            print("⚠️  Таблиці відсутні")
        
        # 3. Статистика таблиць
        if tables:
            print("\n📊 3. СТАТИСТИКА ТАБЛИЦЬ")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)),
                    n_live_tup
                FROM pg_stat_user_tables
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            
            stats = cur.fetchall()
            
            print(f"{'Схема':<15} {'Таблиця':<25} {'Розмір':<15} {'Рядків':<10}")
            print("-" * 65)
            for stat in stats:
                print(f"{stat[0]:<15} {stat[1]:<25} {stat[2]:<15} {stat[3]:<10}")
        
        # 4. Колонки першої таблиці
        if tables:
            print(f"\n📝 4. СТРУКТУРА ТАБЛИЦІ: {tables[0][0]}.{tables[0][1]}")
            print("-" * 80)
            
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """, (tables[0][0], tables[0][1]))
            
            columns = cur.fetchall()
            
            print(f"{'Колонка':<25} {'Тип':<20} {'Nullable':<10} {'За замовчуванням':<20}")
            print("-" * 80)
            for col in columns:
                default = str(col[3])[:18] if col[3] else 'NULL'
                print(f"{col[0]:<25} {col[1]:<20} {col[2]:<10} {default:<20}")
        
        # 5. Первинні ключі
        print("\n🔑 5. ПЕРВИННІ КЛЮЧІ")
        print("-" * 80)
        
        cur.execute("""
            SELECT 
                tc.table_schema,
                tc.table_name,
                STRING_AGG(kcu.column_name, ', ')
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
            GROUP BY tc.table_schema, tc.table_name
        """)
        
        pks = cur.fetchall()
        
        if pks:
            print(f"{'Схема':<20} {'Таблиця':<30} {'Колонки':<30}")
            print("-" * 80)
            for pk in pks:
                print(f"{pk[0]:<20} {pk[1]:<30} {pk[2]:<30}")
        else:
            print("⚠️  Первинні ключі відсутні")
        
        # 6. Індекси
        print("\n📑 6. ІНДЕКСИ")
        print("-" * 80)
        
        cur.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                pg_size_pretty(pg_relation_size(schemaname||'.'||indexname))
            FROM pg_indexes
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY pg_relation_size(schemaname||'.'||indexname) DESC
            LIMIT 10
        """)
        
        indexes = cur.fetchall()
        
        if indexes:
            print(f"{'Схема':<15} {'Таблиця':<25} {'Індекс':<30} {'Розмір':<10}")
            print("-" * 80)
            for idx in indexes:
                print(f"{idx[0]:<15} {idx[1]:<25} {idx[2]:<30} {idx[3]:<10}")
        else:
            print("ℹ️  Індекси відсутні")
        
        # Підсумок
        print("\n" + "=" * 80)
        print("📈 ПІДСУМОК")
        print("=" * 80)
        print(f"Таблиць:         {len(tables)}")
        print(f"Первинних ключів: {len(pks)}")
        print(f"Індексів:        {len(indexes)}")
        
        # Закриття
        cur.close()
        conn.close()
        
        print("\n✅ ПЕРЕВІРКА ЗАВЕРШЕНА!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_database_schema_simple()
