import psycopg2
import os
import sys
from config.db_config import DB_CONFIG


SQL_BASE_DIR = "sql"
DDL_DIR = os.path.join(SQL_BASE_DIR, "ddl")
DML_DIR = os.path.join(SQL_BASE_DIR, "dml")


def create_database():
    """
    Создаёт базу данных, если она не существует
    """
    print("▶ Проверка существования базы данных...")

    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database="postgres"
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG["database"],)
        )

        exists = cur.fetchone()

        if not exists:
            print(f' Создание базы данных "{DB_CONFIG["database"]}"...')
            cur.execute(f'CREATE DATABASE "{DB_CONFIG["database"]}"')
            print("✓ База данных успешно создана")
        else:
            print("✓ База данных уже существует")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print("✗ Ошибка при создании базы данных")
        print(e)
        sys.exit(1)


def execute_sql_from_directory(conn, directory_path, label):
    """
    Выполняет все SQL-файлы из указанной директории
    """
    print(f" Выполнение {label}...")

    if not os.path.exists(directory_path):
        print(f"✗ Каталог не найден: {directory_path}")
        sys.exit(1)

    sql_files = sorted(
        f for f in os.listdir(directory_path) if f.endswith(".sql")
    )

    if not sql_files:
        print(f"✗ В каталоге {directory_path} нет SQL-файлов")
        sys.exit(1)

    cur = conn.cursor()

    for file_name in sql_files:
        file_path = os.path.join(directory_path, file_name)
        print(f"  ▶ {file_name}")

        with open(file_path, "r", encoding="utf-8") as f:
            sql = f.read()
            cur.execute(sql)
            conn.commit()

        print(f"  ✓ {file_name} выполнен")

    cur.close()


def execute_sql_scripts():
    """
    Последовательно выполняет  скрипты по созданию и заполнению таблиц в хранилище данных
    """
    print(" Подключение к целевой базе данных...")

    try:
        conn = psycopg2.connect(**DB_CONFIG)

        execute_sql_from_directory(conn, DDL_DIR, "DDL-скриптов (создание структуры)")
        execute_sql_from_directory(conn, DML_DIR, "DML-скриптов (загрузка данных)")

        conn.close()

    except psycopg2.Error as e:
        print("✗ Ошибка при выполнении SQL-скриптов")
        print(e)
        sys.exit(1)


if __name__ == "__main__":

    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ ХРАНИЛИЩА ДАННЫХ")
    print("Manufacturing Quality Control")
    print("=" * 60)

    create_database()
    execute_sql_scripts()

    print("=" * 60)
    print("ХРАНИЛИЩЕ ДАННЫХ УСПЕШНО СОЗДАНО")
    print("=" * 60)
