import argparse
import os

TASKS_FILE = "tasks.txt"

def load_tasks():
    """Load tasks from the file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_tasks(tasks):
    """Save tasks to the file."""
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def add_task(task):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f" Task added: {task}")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print(" No tasks found.")
        return
    print("\nYour To-Do List:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

def delete_task(index):
    tasks = load_tasks()
    if 1 <= index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f" Task deleted: {removed}")
    else:
        print(" Invalid task number.")

def main():
    parser = argparse.ArgumentParser(description="Simple CLI To-Do List Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="The task to add")

    # View 
    subparsers.add_parser("view", help="View all tasks")

    # Delete 
    delete_parser = subparsers.add_parser("delete", help="Delete a task by number")
    delete_parser.add_argument("index", type=int, help="The task number to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.task)
    elif args.command == "view":
        view_tasks()
    elif args.command == "delete":
        delete_task(args.index)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
