import psycopg2
from config.db_config import DB_CONFIG

def get_all_tables():
    """Подключается к БД и выводит все таблицы со схемами"""
    conn = None
    cur = None

    try:
        # Подключение к базе данных
        print("Подключение к базе данных...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("✓ Успешное подключение к базе данных")
        print(f"Подключено к: {DB_CONFIG.get('database', 'Неизвестная БД')}")
        print("-" * 50)

        # Получение всех таблиц с их схемами
        query = """
        SELECT
            schemaname as schema_name,
            tablename as table_name,
            tableowner as owner
        FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY schemaname, tablename;
        """

        cur.execute(query)
        tables = cur.fetchall()

        # Группировка таблиц по схемам
        tables_by_schema = {}
        for schema, table, owner in tables:
            if schema not in tables_by_schema:
                tables_by_schema[schema] = []
            tables_by_schema[schema].append((table, owner))

        # Вывод результатов
        if not tables_by_schema:
            print("В базе данных нет таблиц (кроме системных)")
        else:
            print(f"НАЙДЕНО ТАБЛИЦ: {sum(len(tables) for tables in tables_by_schema.values())}")
            print()

            for schema in sorted(tables_by_schema.keys()):
                print(f"СХЕМА: {schema}")
                print("-" * 40)

                for i, (table, owner) in enumerate(tables_by_schema[schema], 1):
                    print(f"  {i:2}. {table}")
                    print(f"      Владелец: {owner}")

                print()

        # Дополнительная информация о таблицах
        print("=" * 50)
        print("ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
        print("-" * 50)

        # Количество таблиц по схемам
        cur.execute("""
        SELECT
            schemaname,
            COUNT(*) as table_count
        FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        GROUP BY schemaname
        ORDER BY table_count DESC;
        """)

        schema_counts = cur.fetchall()
        print("\nКоличество таблиц по схемам:")
        for schema, count in schema_counts:
            print(f"  {schema}: {count} таблиц")

        # Общее количество строк во всех таблицах (примерно)
        print("\nПримерное количество строк в таблицах:")
        cur.execute("""
        SELECT
            schemaname,
            relname,
            n_live_tup as estimated_rows
        FROM pg_catalog.pg_stat_user_tables
        ORDER BY n_live_tup DESC
        LIMIT 10;
        """)

        top_tables = cur.fetchall()
        for schema, table, rows in top_tables:
            print(f"  {schema}.{table}: ~{rows:,} строк")

        # Информация о размере таблиц
        print("\nРазмеры таблиц (топ-5 по размеру):")
        cur.execute("""
        SELECT
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) as total_size,
            pg_size_pretty(pg_relation_size(schemaname || '.' || tablename)) as table_size
        FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
        LIMIT 5;
        """)

        table_sizes = cur.fetchall()
        for schema, table, total_size, table_size in table_sizes:
            print(f"  {schema}.{table}: {table_size} (общий: {total_size})")

        # Информация о базе данных
        cur.execute("SELECT version();")
        db_version = cur.fetchone()[0]
        print(f"\nВерсия PostgreSQL: {db_version}")

        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()[0]
        print(f"Текущая база данных: {db_name}")

        cur.execute("SELECT current_user;")
        current_user = cur.fetchone()[0]
        print(f"Текущий пользователь: {current_user}")

    except psycopg2.OperationalError as e:
        print(f"✗ Ошибка подключения к базе данных:")
        print(f"  Сообщение: {e}")
        print("\nПроверьте настройки подключения в config.db_config:")
        for key, value in DB_CONFIG.items():
            if key != 'password':
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: {'*' * len(value) if value else 'не указан'}")

    except psycopg2.Error as e:
        print(f"✗ Ошибка выполнения запроса:")
        print(f"  {e}")

    except KeyError as e:
        print(f"✗ Ошибка конфигурации: отсутствует ключ {e}")
        print("Проверьте файл config.db_config.py")

    except Exception as e:
        print(f"✗ Неизвестная ошибка: {e}")

    finally:
        # Всегда закрываем соединение
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("\n" + "=" * 50)
            print("Соединение с базой данных закрыто")

def get_table_details(schema_name=None, table_name=None):
    """Получает детальную информацию о таблице"""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if table_name and schema_name:
            # Информация о конкретной таблице
            query = """
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length,
                numeric_precision,
                numeric_scale
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position;
            """

            cur.execute(query, (schema_name, table_name))
            columns = cur.fetchall()

            if not columns:
                print(f"Таблица {schema_name}.{table_name} не найдена")
                return

            print(f"\nСТРУКТУРА ТАБЛИЦЫ: {schema_name}.{table_name}")
            print("-" * 60)
            print(f"{'Колонка':<20} {'Тип':<20} {'Null?':<10} {'По умолчанию':<30}")
            print("-" * 60)

            for col in columns:
                nullable = "YES" if col[2] == 'YES' else "NO"
                default = str(col[3]) if col[3] else "-"
                print(f"{col[0]:<20} {col[1]:<20} {nullable:<10} {default:<30}")

    except Exception as e:
        print(f"Ошибка получения информации о таблице: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("СКРИПТ ДЛЯ ПРОСМОТРА ТАБЛИЦ В POSTGRESQL")
    print("=" * 60)
    print()

    # Основная функция - вывод всех таблиц
    get_all_tables()


    print("\n" + "=" * 60)
    print("Работа скрипта завершена")
    print("=" * 60)