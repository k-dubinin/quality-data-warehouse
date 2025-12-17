import psycopg2
import os
import sys
from config.db_config import DB_CONFIG


SQL_DML_DIR = os.path.join("sql", "dml")


def execute_dml_scripts():
    """
    Выполняет DML-скрипты по заполнению измерений и таблицы фактов
    на основе данных из staging-области
    """
    print("▶ Подключение к базе данных...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        if not os.path.exists(SQL_DML_DIR):
            print(f"✗ Каталог DML-скриптов не найден: {SQL_DML_DIR}")
            sys.exit(1)

        sql_files = sorted(
            f for f in os.listdir(SQL_DML_DIR) if f.endswith(".sql")
        )

        if not sql_files:
            print("✗ В каталоге DML нет SQL-файлов")
            sys.exit(1)

        print("▶ Заполнение хранилища данных из staging-области...")

        for file_name in sql_files:
            file_path = os.path.join(SQL_DML_DIR, file_name)
            print(f"  ▶ Выполнение {file_name}...")

            with open(file_path, "r", encoding="utf-8") as f:
                sql = f.read()
                cur.execute(sql)
                conn.commit()

            print(f"  ✓ {file_name} выполнен успешно")

        cur.close()
        conn.close()

        print("✓ Загрузка данных в хранилище завершена успешно")

    except psycopg2.Error as e:
        print("✗ Ошибка при выполнении DML-скриптов")
        print(e)
        if conn:
            conn.rollback()
            conn.close()
        sys.exit(1)


if __name__ == "__main__":

    print("=" * 60)
    print("ЗАГРУЗКА ДАННЫХ В ХРАНИЛИЩЕ ДАННЫХ")
    print("ИЗ STAGING-ОБЛАСТИ")
    print("=" * 60)

    execute_dml_scripts()

    print("=" * 60)
    print("ХРАНИЛИЩЕ ДАННЫХ УСПЕШНО ЗАПОЛНЕНО")
    print("=" * 60)
