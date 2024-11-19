import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
from datetime import datetime


root = tk.Tk()
root.title("Aesthetic To-Do List")
root.geometry("500x600")
root.config(bg="#f9f5eb")  


TASKS_FILE = "tasks.json"


FONT = ("Helvetica", 12)
HIGHLIGHT_COLOR = "#9fedd7"
TEXT_COLOR = "#383e56"
DARK_BG = "#2e2e2e"
DARK_FG = "#f0f0f0"


dark_mode = False


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.config(bg=DARK_BG)
        task_listbox.config(bg="#3e3e3e", fg=DARK_FG)
        add_button.config(bg="#444", fg=DARK_FG)
        delete_button.config(bg="#444", fg=DARK_FG)
        clear_button.config(bg="#444", fg=DARK_FG)
        edit_button.config(bg="#444", fg=DARK_FG)
        complete_button.config(bg="#444", fg=DARK_FG)
        filter_menu.config(bg="#444", fg=DARK_FG)
    else:
        root.config(bg="#f9f5eb")
        task_listbox.config(bg="#fff", fg=TEXT_COLOR)
        add_button.config(bg="#9fedd7", fg="black")
        delete_button.config(bg="#e58c8a", fg="black")
        clear_button.config(bg="#f4a261", fg="black")
        edit_button.config(bg="#f8b400", fg="black")
        complete_button.config(bg="#90be6d", fg="black")
        filter_menu.config(bg="#9fedd7", fg="black")


tasks = load_tasks()


def add_task():
    task = simpledialog.askstring("New Task", "Enter your task:", parent=root)
    if task:
        due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):", parent=root)
        tasks.append({"task": task, "completed": False, "due_date": due_date})
        update_task_list()
        save_tasks()


def edit_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        current_task = tasks[selected_task_index]
        new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=current_task["task"])
        if new_task:
            tasks[selected_task_index]["task"] = new_task
            update_task_list()
            save_tasks()
    except IndexError:
        messagebox.showwarning("Edit Task", "Please select a task to edit.")


def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks.pop(selected_task_index)
        update_task_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Delete Task", "Please select a task to delete.")


def clear_all_tasks():
    confirm = messagebox.askyesno("Clear All Tasks", "Are you sure you want to delete all tasks?")
    if confirm:
        tasks.clear()
        update_task_list()
        save_tasks()


def mark_as_complete():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks[selected_task_index]["completed"] = True
        update_task_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Complete Task", "Please select a task to mark as complete.")


def filter_tasks(*args):
    filter_option = filter_var.get()
    update_task_list(filter_option)


def update_task_list(filter_option="All"):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        if filter_option == "Completed" and not task["completed"]:
            continue
        elif filter_option == "Pending" and task["completed"]:
            continue
        display_text = f"{task['task']} - Due: {task['due_date']}"
        if task["completed"]:
            display_text += " [✓]"
        task_listbox.insert(tk.END, display_text)


frame = tk.Frame(root, bg="#f9f5eb")
frame.pack(pady=20)


task_listbox = tk.Listbox(
    frame,
    font=FONT,
    width=40,
    height=10,
    bg="#fff",
    fg=TEXT_COLOR,
    selectbackground=HIGHLIGHT_COLOR
)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)


scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)


button_frame = tk.Frame(root, bg="#f9f5eb")
button_frame.pack(pady=10)


add_button = tk.Button(button_frame, text="Add Task", command=add_task, font=FONT, bg="#9fedd7")
add_button.grid(row=0, column=0, padx=5)

edit_button = tk.Button(button_frame, text="Edit Task", command=edit_task, font=FONT, bg="#f8b400")
edit_button.grid(row=0, column=1, padx=5)

complete_button = tk.Button(button_frame, text="Mark Complete", command=mark_as_complete, font=FONT, bg="#90be6d")
complete_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, font=FONT, bg="#e58c8a")
delete_button.grid(row=1, column=0, padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear All", command=clear_all_tasks, font=FONT, bg="#f4a261")
clear_button.grid(row=1, column=1, padx=5)

dark_mode_button = tk.Button(button_frame, text="Toggle Dark Mode", command=toggle_dark_mode, font=FONT, bg="#444", fg="#f0f0f0")
dark_mode_button.grid(row=1, column=2, padx=5)


filter_var = tk.StringVar()
filter_var.set("All")
filter_menu = ttk.Combobox(button_frame, textvariable=filter_var, values=["All", "Completed", "Pending"], state='readonly')
filter_menu.grid(row=2, column=1, pady=10)
filter_menu.bind("<<ComboboxSelected>>", filter_tasks)


update_task_list()


root.mainloop()
