# --- Importing --- #
import os
import psycopg

def get_connection():
    return psycopg.connect(
        dbname="task_manager",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        host="localhost"
    )

# --- Functions --- #

def display_menu():
    print("\n========================")
    print("    TASK MANAGER v3")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def present_task(tasks):

    print("\nTASK LIST")

    print()

    for task in tasks:
        status = "Completed" if task[2] else "Not Completed"
        print(f"{task[0]}. {task[1]} - {status}")

def add_task():
    title = input("Enter task: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title) VALUES (%s)",
        (title,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    print("Task added successfully!")

def view_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id ASC"
    )

    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
    else:
        present_task(tasks)

    cursor.close()
    conn.close()

def complete_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks"
    )

    tasks = cursor.fetchall()

    if tasks:
        present_task(tasks)

        task_id = int(input("\nEnter the task ID to complete: "))
        cursor.execute(
            "UPDATE tasks SET completed = TRUE WHERE id = %s", 
            (task_id,)
        )

        if cursor.rowcount == 0:
            print(f"Task {task_id} not found.")
        else:
            conn.commit()
            print(f"Task {task_id} marked completed!")

    else:

        print("No tasks found.")

    cursor.close()
    conn.close()
    
def delete_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, title, completed FROM tasks"
    )
    
    tasks = cursor.fetchall()

    if not tasks:
        print("No tasks found.")
    else:
        present_task(tasks)

        task_id = int(input("\nEnter the task ID to delete: "))
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

        if cursor.rowcount == 0:
            print(f"Task {task_id} not found.")
        else:
            conn.commit()
            print(f"Task {task_id} deleted successfully.")

    cursor.close()
    conn.close()


def main():

    while True:

        display_menu()
        choice = input("\n Choose an option: ")

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            complete_tasks()

        elif choice == "4":
            delete_tasks()

        elif choice == "5":
            print("Goodbye, Levi! Thanks for using Task Manager!")
            break

        else:
            print("Wrong Input. Please enter only the numbers provided.")


# Working on JSON saving feature

if __name__ == "__main__":
    main()
