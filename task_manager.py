
import os
from datetime import datetime, date

# Define datetime format
DATETIME_STRING_FORMAT = "%Y-%m-%d"


# Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please try again.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added.")
        username_password[new_username] = new_password
        # Append new user to user.txt
        with open("user.txt", "a") as user_file:
            user_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match.")


# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username.")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified.")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    # Append new task to tasks.txt
    with open("tasks.txt", "a") as task_file:
        str_attrs = [
            new_task['username'],
            new_task['title'],
            new_task['description'],
            new_task['due_date'].strftime(DATETIME_STRING_FORMAT),
            new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "No"
        ]
        task_file.write("\n" + ";".join(str_attrs))
    print("Task successfully added.")


# Function to view all tasks
def view_all():
    for t in task_list:
        print("*" * 75)
        disp_str = f"\nTask: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# Function to update task status and edit task details in tasks.txt
def update_task_file(task_list):
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            task_file.write(";".join(str_attrs) + "\n")


# Function to view tasks assigned to the current user
def view_mine():
    for idx, t in enumerate(task_list):
        if t['username'] == curr_user:
            print("*" * 75)
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t \
                {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(f"{idx + 1}. {disp_str}")
    selected_task = input\
        ("Enter the number of the task you want to select or -1 to return to the main menu: ")
    if selected_task.isdigit():
        selected_task = int(selected_task)
        if selected_task == -1:
            return
        elif 0 < selected_task <= len(task_list):
            task_to_edit = task_list[selected_task - 1]
            action = input("Do you want to mark this task as complete\
                     (enter 'mark') or edit this task (enter 'edit')? ")
            if action == "mark":
                task_to_edit['completed'] = True
                print("Task marked as complete.")
            elif action == "edit":
                if not task_to_edit['completed']:
                    new_username = input("Enter the new username or press enter to \
                                         keep the current username: ")
                    new_due_date = input\
                    ("Enter the new due date in the format YYYY-MM-DD or \
                     press enter to keep the current due date: ")
                    if new_username:
                        task_to_edit['username'] = new_username
                    if new_due_date:
                        try:
                            task_to_edit['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            print("Task updated successfully.")
                        except ValueError:                
                            print("Invalid date format. Task not updated.")
                    # Update tasks.txt after editing task
                    update_task_file(task_list)        
                else:
                    print("Completed tasks cannot be edited.")
        else:
            print("Invalid task number.")
    else:
        print("Invalid input. Please enter a valid task number.")


# Function to display statistics
def display_statistics():
    if curr_user != 'admin':
        print("You do not have permission to access this feature.")
        return

    task_overview_data, user_overview_data = generate_reports()
    
    if task_overview_data:
        print("\nTask Overview:\n")
        print(task_overview_data)
    else:
        print("Error: Task overview data not generated.")

    if user_overview_data:
        print("\nUser Overview:\n")
        print(user_overview_data)
    else:
        print("Error: User overview data not generated.")

    print("\n" + "*" * 75)


## Function to generate reports
def generate_reports():
    try:
        task_overview = {
            "Total Tasks": len(task_list),
            "Completed Tasks": sum(1 for t in task_list if t['completed']),
            "Uncompleted Tasks": sum(1 for t in task_list if not t['completed']),
            "Overdue Tasks": sum(1 for t in task_list if not t['completed']\
                                  and t['due_date'] < datetime.combine(date.today(),\
                                                                        datetime.min.time())),
            "Percentage Incomplete": round((sum(1 for t in task_list\
                                                 if not t['completed']) / len(task_list)) * 100, 2),
            "Percentage Overdue": round((sum(1 for t in task_list if not t['completed']\
                                    and t['due_date'] < datetime.combine(date.today(),\
                                     datetime.min.time())) / len(task_list)) * 100, 2)
        }
        with open("task_overview.txt", "w") as task_overview_file:
            for k, v in task_overview.items():
                task_overview_file.write(f"{k}: {v}\n")
        task_overview_data = "\n".join([f"{k}: {v}" for k, v in task_overview.items()])
    except FileNotFoundError:
        print("Error: Task overview file not found")
        task_overview_data = ""

    try:
        user_overview = {}
        for username in username_password.keys():
            user_tasks = [t for t in task_list if t['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
            if total_user_tasks == 0:  # Check if total_user_tasks is zero
                user_overview[username] = {
                    "Total Tasks": 0,
                    "Percentage Total": 0,
                    "Percentage Completed": 0,
                    "Percentage Incomplete": 0,
                    "Percentage Overdue": 0
                }
            else:
                overdue_user_tasks = sum(1 for t in user_tasks if not t['completed']\
                                          and t['due_date'] < datetime.combine(date.today(),\
                                                                                datetime.min.time()))
                user_overview[username] = {
                    "Total Tasks": total_user_tasks,
                    "Percentage Total":\
                          round((total_user_tasks / len(task_list)) * 100, 2),
                    "Percentage Completed": \
                        round((completed_user_tasks / total_user_tasks) * 100, 2),
                    "Percentage Incomplete":\
                          round(((total_user_tasks - completed_user_tasks) / total_user_tasks) * 100, 2),
                    "Percentage Overdue":\
                          round((overdue_user_tasks / total_user_tasks) * 100, 2)
                }
        with open("user_overview.txt", "w") as user_overview_file:
            user_overview_file.write(f"Total Users: {len(username_password)}\n")
            for username, overview in user_overview.items():
                user_overview_file.write(f"User: {username}\n")
                user_overview_file.write("\n".join([f"{k}: {v}"\
                                                     for k, v in overview.items()]) + "\n")
        user_overview_data = ""
        for username, overview in user_overview.items():
            user_overview_data += f"User: {username}\n"
            user_overview_data = "\n".join([f"\nUser: {username}\n\n" \
                                            + "\n".join([f"{k}: {v}" for k, v in overview.items()])\
                                                  for username, overview in user_overview.items()])
    except FileNotFoundError:
        print("Error: User overview file not found")
        user_overview_data = ""

    return task_overview_data, user_overview_data



# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Read tasks data from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


# Populate task_list
task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3],\
                                            DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4],\
                                                 DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(curr_t)


# Create user.txt if it doesn't exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")


# Read user data from user.txt
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")


# Populate username_password dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password


# Login process
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Main loop for user interaction
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'ds':
        display_statistics()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")

