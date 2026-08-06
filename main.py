def display_menu():
    print("\n========================")
    print("         TASK MANAGER")
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
                for i in range(len(tasks)):
                    print(f"{i + 1}. {tasks[i]}")

        elif choice == "4":
            print("Goodbye!")
            break


        else:
            print("Feature coming soon!")


if __name__ == "__main__":
    main()