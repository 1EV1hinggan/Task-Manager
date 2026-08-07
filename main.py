def display_menu():
    print("\n========================")
    print("    TASK MANAGER v2")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Tasks")
    print("4. Exit")

tasks = []

def main():
    while True:
        display_menu()
        choice = input("\nChoose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            print("Task added successfully!")

        elif choice == "2":
            if not tasks:
                print("No task found.")

            else:
                print("\nTASK LIST")
                for i in range(len(tasks)):
                    print(f"{i + 1}. {tasks[i]}")

        elif choice == "3":
            if not tasks:
                print("No task/s to delete.")
                continue
            else:
                print("\nTASK LIST")
                for i in range(len(tasks)):
                    print(f"{i + 1}. {tasks[i]}")

            num_del = int(input("\nEnter the task's number to delete: "))

            if num_del < 1 or num_del > len(tasks):
                print("Invalid task number.")

            else:
                tasks.pop(num_del - 1)
                print("Task deleted successfully!")

        elif choice == "4":
            print("Goodbye! See you next time!")
            break


        else:
            print("Feature coming soon!")

# Working on JSON saving feature

if __name__ == "__main__":
    main()
