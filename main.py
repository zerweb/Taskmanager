import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tasks.db"


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK(length(trim(title)) > 0),
                is_done INTEGER NOT NULL DEFAULT 0 CHECK(is_done IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_task():
    title = input("Введите название задачи: ").strip()
    if not title:
        print("Ошибка: название задачи не может быть пустым.")
        return
    with connect() as connection:
        connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    print("Задача добавлена!")


def show_tasks():
    with connect() as connection:
        tasks = connection.execute(
            "SELECT id, title, is_done, created_at FROM tasks ORDER BY id"
        ).fetchall()
    if not tasks:
        print("Список задач пуст.")
        return
    print("\nСписок задач:")
    for task in tasks:
        status = "✓" if task["is_done"] else " "
        print(f'{task["id"]}. [{status}] {task["title"]} (создана: {task["created_at"]})')


def read_task_id():
    value = input("Введите ID задачи: ").strip()
    try:
        task_id = int(value)
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        print("Ошибка: ID должен быть положительным целым числом.")
        return None


def complete_task():
    task_id = read_task_id()
    if task_id is None:
        return
    with connect() as connection:
        cursor = connection.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
    print("Задача выполнена!" if cursor.rowcount else "Задача с таким ID не найдена.")


def delete_task():
    task_id = read_task_id()
    if task_id is None:
        return
    with connect() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    print("Задача удалена!" if cursor.rowcount else "Задача с таким ID не найдена.")


def main():
    init_db()
    while True:
        print("\n=== TaskManager (SQLite) ===")
        print("1. Добавить задачу")
        print("2. Показать задачи")
        print("3. Отметить задачу выполненной")
        print("4. Удалить задачу")
        print("0. Выход")
        try:
            choice = input("Выберите действие: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            break
        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда. Введите число от 0 до 4.")


if __name__ == "__main__":
    main()
