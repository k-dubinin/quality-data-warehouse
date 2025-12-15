import psycopg2
from config.db_config import DB_CONFIG
import sys

def load_csv_to_postgres(csv_file_path):

    copy_sql = """
    COPY stg.manufacturing_quality_raw (
    batch_id,
    production_date,
    product_code,
    shift,
    operator_id,
    inspection_id,
    inspection_date,
    inspector_id,
    quality_score,
    defect_type,
    defect_severity,
    defect_count,
    rework_required,
    comments,
    factory_location
)
FROM STDIN
WITH (
    FORMAT CSV,
    DELIMITER ',',
    HEADER TRUE,
    ENCODING 'UTF8'
)
    """

    conn = None
    try:
        print(f"Подключение к базе данных {DB_CONFIG['database']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✓ Подключение успешно")

        print(f"Открытие файла {csv_file_path}...")
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            print("✓ Файл открыт, начинается загрузка...")
            cur.copy_expert(copy_sql, f)
            conn.commit()
        cur.execute("SELECT COUNT(*) FROM stg.manufacturing_quality_raw")
        count = cur.fetchone()[0]

        print(f"Загрузка завершена успешно!")
        print(f"Загружено строк в таблицу: {count}")

        cur.close()

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {csv_file_path}")
        print("Проверьте путь к файлу")
        sys.exit(1)

    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        print("Проверьте параметры подключения в config.db_config")
        sys.exit(1)

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            print("Соединение с БД закрыто")

if __name__ == "__main__":
    csv_file = "data/processed/manufacturing_quality_clean.csv"

    print("=" * 60)
    print("ЗАГРУЗКА CSV В POSTGRESQL")
    print("=" * 60)

    load_csv_to_postgres(csv_file)

    print("=" * 60)
    print("СКРИПТ ВЫПОЛНЕН")
    print("=" * 60)