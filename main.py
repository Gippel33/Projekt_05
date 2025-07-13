# projekt_05.py: pázý projekt do Engeto Online Python Akademie

# author: Pavel Nováček
# email: gippel@seznam.cz


from functions import create_table_if_not_exists, main_menu, add_task, \
                      add_task_input, display_all_tasks, check_id, \
                      update_task_input, update_task, delete_task, \
                      delete_task_input


def main():
    """
    Main run of the program, which runs functions by the choice.
    """
    create_table_if_not_exists()
    while True:
        choice = main_menu()
        if choice == 1:
            result_add = add_task_input()
            name, description = result_add
            if name is not None:
                add_task(name, description)
        elif choice == 2:
            display_all_tasks()
        elif choice == 3:
            result_update = update_task_input()
            task_id, new_status = result_update
            if task_id is not None:
                print(task_id, check_id(task_id))
                update_task(task_id, new_status)
        elif choice == 4:
            delete_id = delete_task_input()
            if delete_id is not None:
                delete_task(delete_id)
        elif choice == 5:
            print("\nQuiting the program.\n")
            exit()


if __name__ == "__main__":
    main()
