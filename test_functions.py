from datetime import datetime

import mysql.connector
from mysql.connector import Error
from mysql.connector.errors import IntegrityError, DatabaseError
import pytest

from config import load_config
from db import connect_to_db
from functions import display_all_tasks, add_task, update_task, delete_task


# Vytvoření testovací tabulky
def create_table_if_not_exists(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id int auto_increment Primary key,
            name varchar(100) not null unique,
            description text not null,
            status enum ('not started', 'in progress', 'completed')
            default 'not started',
            date DATE not null,
            CHECK (CHAR_LENGTH(name) > 0),
            CHECK (CHAR_LENGTH(description) > 0)
                       )
                       """)
    except Error as e:
        print(f"Error creating a table: {e}")


# Připojení do testovací databáze
@pytest.fixture(scope="module")
def db_conn():
    config = load_config(testing=True)
    conn = connect_to_db(config)
    cursor = conn.cursor()
    create_table_if_not_exists(cursor)
    cursor.close()
    yield conn
    conn.rollback()
    conn.close()


# Vyčištění tabulky
@pytest.fixture(autouse=True)
def clear_test_data(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE tasks")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    db_conn.commit()
    cursor.close()


def test_add_task_positive(db_conn):
    add_task("Test1", "Positive_test", "not started")
    add_task("Test2", "Positive_test", "in progress")
    add_task("Test3", "Positive_test", "completed")
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 3


def test_add_task_negative_1(db_conn):
    add_task("Test1", "Negative_test", "not started")
    with pytest.raises(IntegrityError):
        add_task("Test1", "Negative_test", "not started")
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 1


def test_add_task_negative_2(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    with pytest.raises(IntegrityError):
        add_task("Test1", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 1


def test_add_task_negative_3(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    with pytest.raises(DatabaseError):
        add_task("", "Negative_test", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 1


def test_update_task_positive_in_progress(db_conn):
    add_task("Test1", "Positive_test", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_id = tasks[0][0]
    update_task(task_id, "in progress", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_status = tasks[0][3]
    assert task_status == "in progress"


def test_update_task_positive_completed(db_conn):
    add_task("Test1", "Positive_test", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_id = tasks[0][0]
    update_task(task_id, "completed", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_status = tasks[0][3]
    assert task_status == "completed"


def test_update_task_negative_id(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    update_task("999", "in progress")
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_status = tasks[0][3]
    assert task_status == "not started"


def test_update_task_negative_status(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_id = tasks[0][0]
    with pytest.raises(DatabaseError):
        update_task(task_id, "failed")
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_status = tasks[0][3]
    assert task_status == "not started"


def test_delete_task_positive(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    task_id = tasks[0][0]
    delete_task(task_id, conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 0


def test_delete_task_negative(db_conn):
    add_task("Test1", "Negative_test", "not started", conn=db_conn)
    delete_task("999", conn=db_conn)
    tasks = display_all_tasks(conn=db_conn, interactive=False)
    assert len(tasks) == 1
