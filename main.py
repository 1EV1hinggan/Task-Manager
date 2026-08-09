# --- Importing --- #
import os

from database import SessionLocal
from models import Task
from sqlalchemy import select

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

    print("\nTASK LIST\n")

    for task in tasks:
        status = "Completed" if task.completed else "Not Completed"

        print(f"{task.id}. {task.title} - {status}")

def add_task():
    title = input("Enter task: ")

    with SessionLocal() as session:
        new_task = Task(title=title)

        session.add(new_task)
        session.commit()

    print("Task added successfully!")

def view_tasks():
    with SessionLocal() as session:
            result = session.execute(
                select(Task).order_by(Task.id)
            )

            tasks = result.scalars().all()

            if not tasks:
                print("No task found.")
            else:
                present_task(tasks)

def complete_tasks():
    with SessionLocal() as session:

        result = session.execute(
            select(Task).order_by(Task.id)
        )

        tasks = result.scalars().all()

        if not tasks:
            print("No task found.")
            return

        present_task(tasks)

        task_id = int(input("\nEnter task ID to complete: "))

        task = session.get(Task, task_id)

        if task is None:
            print(f"Task {task_id} not found.")

        elif task.completed:
            print(f"Task {task_id} is already completed.")

        else:
            task.completed = True

            session.commit()

            print(f"Task {task_id} marked complete.")
    
def delete_tasks():
    with SessionLocal() as session:

        result = session.execute(
            select(Task).order_by(Task.id)
        )

        tasks = result.scalars().all()

        if not tasks:
            print("No task found.")
            return

        present_task(tasks)

        task_id = int(input("\nEnter the task ID to delete: "))

        task = session.get(Task, task_id)

        if task is None:
            print(f"Task {task_id} not found.")

        else:
            session.delete(task)
            session.commit()

            print(f"Task {task_id} deleted successfully.")

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
