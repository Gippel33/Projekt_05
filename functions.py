from datetime import datetime


import mysql.connector
from mysql.connector import Error


from db import connect_to_db


# Hlavní menu
def main_menu():
    """
    Displays main menu and enables to choose a function due to the choice 1-4.
    """

    while True:
        print("Task manager - main menu",
              "1. Add a task",
              "2. Display all tasks",
              "3. Update a task",
              "4. Delete a task",
              "5. Quit program",
              sep="\n"
              )
        try:
            entry = int(input("Enter 1-5: "))
            if entry not in (1, 2, 3, 4, 5):
                print("Choice out of range. Enter a number 1-5.\n")
                continue
            return entry
        except ValueError:
            print("Invalid choice. Enter a number 1-5.\n")
            continue


# Vytvoření tabulky pokud neexistuje
def create_table_if_not_exists(conn=None):
    """
    Creates the task table if ot doesnt exist.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()

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

        conn.commit()

    except Error as e:
        print(f"Error creating a table: {e}")


# Přidání úkolu
def add_task_input():
    """
    Returns user input for a task - name, description.

    Example:
    Enter a taks name: Test1
    Enter a task description: This is test.
    """

    while True:
        print("To return to the main menu, enter 'z'")
        name = input("Enter a task name: ")
        if name == "":
            print("Empty entry. Please enter a task name.\n")
            continue
        elif name == "z":
            print()
            return None, None
        description = input("Enter a task description: ")
        if description == "":
            print("Empty entry. Please enter a task description.\n")
            continue
        return name, description


def add_task(name, description, status='not started', conn=None):
    """
    Adds a task in the format: name and description.

    Example:
    Task name: Test1
    Task description: This is test.
    """
    today = datetime.today().date()

    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, description, status, date) "
                   "VALUES (%s, %s, %s, %s)",
                   (name, description, status, today))
    conn.commit()

    print(f"The task {name} has been added.\n")
    cursor.close()
    if close_conn:
        conn.close()


# Zobrazení úkolů
def display_all_tasks(conn=None, interactive=True):
    """
    Displays all tasks.
    """

    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks_list = cursor.fetchall()

    cursor.close()
    if close_conn:
        conn.close()

    if len(tasks_list) == 0:
        print("Tasks list is empty.\n")
        return []
    else:
        display_tasks_format(tasks_list)

    if not interactive:
        return tasks_list
    else:
        while True:
            try:
                choice = input("Do you wish to filter tasks by status? "
                               "y/n: ").lower()
                if choice == "y":
                    filter_tasks_by_status(filter_tasks_by_status_input())
                    break
                elif choice == "n":
                    print()
                    break
                else:
                    print("Invalid entry. Enter y/n.\n")
                    continue
            except ValueError:
                print("Invalid entry. Enter y/n.\n")


def display_tasks_format(tasks_list):
    """
    Iterates list and prints each task in format.

    Example:
    ID: 1
    Name: Test1
    Description: This is test1.
    Date: 2025-7-25
    """
    for task in tasks_list:
        task_id = task[0]
        task_name = task[1]
        task_description = task[2]
        task_status = task[3]
        task_date = task[4]
        print(f"ID: {task_id}\nName: {task_name} \
              \nDescription: {task_description} \
              \nStatus: {task_status}\nCreated: {task_date}\n")


# Filtr úkolů
def filter_tasks_by_status_input():
    """
    Returns status to update.
    not started, in progress or completed
    """
    while True:
        try:
            choice = int(input("Choose which status to be filtered "
                               "1 - not started, "
                               "2 - 'in progress', "
                               "3 - 'completed': "))
            if choice == 1:
                return 'not started'
            elif choice == 2:
                return 'in progress'
            elif choice == 3:
                return 'completed'
            else:
                print("Invalid entry. Enter a number 1-3.\n")
                continue
        except ValueError:
            print("Invalid entry. Enter a number 1-3.\n")
            continue


def filter_tasks_by_status(status, conn=None):
    """
    Fitlers tasks by status.
    not started, in progress or completed
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    query = "SELECT * from tasks where status = %s"
    cursor.execute(query, (status,))
    tasks_list = cursor.fetchall()

    cursor.close()
    if close_conn:
        conn.close()

    if not tasks_list:
        print("There is no task with this status.\n")
    else:
        display_tasks_format(tasks_list)


# Kontrola ID
def check_id(task_id, conn=None):
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    query = "SELECT * from tasks where id = %s"
    cursor.execute(query, (task_id,))
    task = cursor.fetchone()

    cursor.close()
    if close_conn:
        conn.close()

    if not task:
        print("⚠️ A task with this ID doesn't exist.\n")
        return False
    else:
        return True


# Update úkolu
def update_task_input():
    """
    Returns task id and status to update a task.
    """

    display_all_tasks(conn=None)

    while True:
        print("To return to the main menu, enter 'z'")
        try:
            task_id = input("Enter a task number you wish to update: ")
            if task_id == "z":
                print()
                return None, None
            elif not check_id(task_id):
                continue
            if task_id:
                status = int(input(
                    "Choose new status: 1 - In progress, 2 - Completed: "))
                if status not in (1, 2):
                    print("Invalid entry. Enter 1 or 2.")
                    continue
                if status == 1:
                    return task_id, "in progress"
                elif status == 2:
                    return task_id, "completed"
        except ValueError:
            print("Invalid entry. Enter a number.\n")
            continue


def update_task(task_id, new_status, conn=None):
    """
    Updates the task status.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s",
                   (new_status, task_id))
    conn.commit()

    print(f"The task {task_id} has been updated.\n")
    cursor.close()
    if close_conn:
        conn.close()


# Vymazání úkolu
def delete_task_input():
    """
    Returns tasks id for deletion.
    """

    display_all_tasks(conn=None)

    while True:
        print("To return to the main menu, enter 'z'")
        try:
            task_id = input("Enter a task number you wish to delete: ")
            if task_id == "z":
                print()
                return None
            elif not check_id(task_id):
                continue
            else:
                return task_id
        except ValueError:
            print("Invalid entry. \
                   Enter a task number in the tasks list range.\n")
            continue


def delete_task(task_id, conn=None):
    """
    Deletes the task from the tasks list by task id.
    """
    close_conn = False
    if conn is None:
        conn = connect_to_db()
        close_conn = True

    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(query, (task_id,))
    conn.commit()

    print(f"The task {task_id} has been deleted.\n")

    cursor.close()
    if close_conn:
        conn.close()
