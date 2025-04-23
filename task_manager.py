# ===== Importing external modules ===========
from datetime import datetime

# ===== Functions =====


def reg_user(users):

    '''
    This code block will add a new user to the user.txt file
    Check if the new password and confirmed password are the same
    If they are the same, add them to the user.txt file,
    otherwise present a relevant error message
    '''

    while True:
        new_username = input("Enter new user's username: ")
        # checks if username already exists
        if new_username in users:
            print("This username already exists. Try something else.")
            continue
        else:
            break
    while True:
        new_password = input("Enter new user's password: ")
        confirmation = input("Confirm password: ")
        # check if user entered the same password to ensure correct credentials
        if new_password == confirmation:
            # stores correct user credentials in a variable to add to database
            new_user_login = (new_username, new_password)

            # opens user.txt and adds new users user credentials
            try:
                with open("user.txt", "a", encoding="utf-8") as file:
                    file.write("\n" + ", ".join(new_user_login))
                    users[new_username] = new_password
                    print(f"\nYou have successfully added {new_username} as a user\n")
            except FileNotFoundError:
                print("This file does not exist.")
            break
        else:
            print("Passwords dont match. Please try again.")


def add_task(users):

    '''
    This code block will allow a user to add a new task to task.txt file
    By getting all the relevant data required to create a new task
    then add the data to the file task.txt
    '''

    while True:
        assigned_user = input("Enter the username of the user you would like to assign a task to: ")
        # checks if the user entered a valid username that exists on the system
        if assigned_user in users:
            break
        else:
            print("User not found. Try again")

    # this block of code prompts the user to enter all the necessary data
    # required to create a new task
    task_title = input("Enter a task title: ")
    task_description = input("Enter a task description: ")
    while True:
        task_due_date = input("By when is this task due?\n Use the following format [dd mmm yyyy]: ")
        try:
            due_date = datetime.strptime(task_due_date, "%d %b %Y").date()  # convert date to correct format
            print("Valid date entry.")
            break
        except ValueError:
            print("incorrect date format. Please try again.")
        except TypeError:
            print("incorrect date format. Please try again.")
    today = datetime.now()  # generate current time
    formatted_date = (today.strftime("%d %b %Y"))  # converts current date to correct format
    complete = "No"
    # capture all the data needed to create a new task in one variable
    new_task = (assigned_user, task_title, task_description, formatted_date, due_date.strftime('%d %b %Y'), complete)

    # open tasks.txt file and append the task data to it
    try:
        with open("tasks.txt", "a", encoding="utf-8") as file:
            file.write("\n" + ", ".join(new_task))
            print(f"Task successfully added. Due on: {due_date.strftime('%d %b %Y')}")
    except FileNotFoundError:
        print("File does not exist.")


def view_all():

    '''
    This code block will read the task from task.txt file
    and print it out to the console
    '''
    # open tasks.txt and captures all the tasks into a list called data
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            data = []
            for line in file:
                data.append(line.strip().split(","))
            print("─" * 80 + "\n")
            # iterate through every task in the data list and print each task
            for lists in data:
                print(f'''Task:                        {lists[1]}
Assigned to:                  {lists[0]}
Date assigned:               {lists[3]}
Due date:                    {lists[4]}
Task complete?               {lists[5]}
Task description:
{lists[2]}''')
                print("\n" + "─" * 80 + "\n")
    except FileNotFoundError:
        print("File does not exist")


def view_mine(input_username):
    '''
    View and manage tasks assigned to the logged-in user.
    Task numbers are local to the user, starting from 1.
    '''

    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            data = [line.strip().split(",") for line in file if line.strip()]
    except FileNotFoundError:
        print("File does not exist.")
        return

    user_tasks = []
    print("─" * 80 + "\n")
    display_index = 1

    for i, task in enumerate(data):  # i = actual index in file
        if task[0].strip() == input_username:
            user_tasks.append((display_index, i, task))  # (user-facing number, actual index, task)
            print(f'''#{display_index}.
Task:                        {task[1].strip()}
Assigned to:                 {task[0].strip()}
Date assigned:               {task[3].strip()}
Due date:                    {task[4].strip()}
Task complete?               {task[5].strip()}
Task description:
{task[2].strip()}''')
            print("\n" + "─" * 80 + "\n")
            display_index += 1

    if not user_tasks:
        print("You have no active tasks.\n")
        return

    try:
        choice = int(input('''Enter the number of the task you wish to edit
or enter -1 to return: '''))
    except ValueError:
        print("Invalid input.")
        return

    if choice == -1:
        print("Returning to the menu...\n")
        return

    # Find the selected task
    selected_task_entry = None
    for entry in user_tasks:
        if entry[0] == choice:
            selected_task_entry = entry
            break

    if not selected_task_entry:
        print("Invalid task number.")
        return

    display_num, data_index, selected_task = selected_task_entry

    # If task is already complete, prevent edits
    if selected_task[5].strip().lower() == "yes":
        print("This task has already been completed and cannot be edited.\n")
    else:
        print("What would you like to do?")
        print("1 - Mark task as complete")
        print("2 - Edit the task (Assign the task to another user)")
        action = input("Select option: ")

        if action == "1":
            selected_task[5] = "Yes"
            data[data_index] = selected_task
            print("Task marked as complete.")
        elif action == "2":
            # Edit assigned user
            while True:
                new_user = input("Enter new username (leave blank to keep current): ").strip()
                if new_user in users:
                    break
                else:
                    print("User not found. Try again")
            # Edit due date
            while True:
                input_due_date = input("Enter new due date (leave blank to keep current): ").strip()
                try:
                    new_due_date = datetime.strptime(input_due_date, "%d %b %Y").date()
                    print("Valid date entry.")
                    break
                except ValueError:
                    print("incorrect date format. Please try again.\n Use the following format [dd mmm yyyy]")
                except TypeError:
                    print("incorrect date format. Please try again.\n Use the following format [dd mmm yyyy]")

            if new_user:
                selected_task[0] = new_user
            if new_due_date:
                selected_task[4] = new_due_date.strftime('%d %b %Y')

            data[data_index] = selected_task
            print("Task updated.")
        else:
            print("No action taken.")

    # Write updated data back to file
    if len(data) > 1:
        try:
            with open("tasks.txt", "w", encoding="utf-8", newline="") as file:
                file.write(", ".join(str(item).strip() for item in data[0]))
                for row in data[1:]:
                    file.write("\n" + ", ".join(str(item).strip() for item in row))
        except FileNotFoundError:
            print("This file does not exist.")
    elif len(data) == 1:
        try:
            with open("tasks.txt", "w", encoding="utf-8", newline="") as file:
                file.write(", ".join(str(item).strip() for item in data[0]))
        except FileNotFoundError:
            print("This file does not exist.")
    else:
        print("Task deleted. You have no active tasks left.")


def view_completed():

    '''
    This code will read the tasks from task.txt file
    and check if there are any tasks with completed status of "Yes"
    then print all completed tasks
    '''

    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            data = []
            for line in file:
                data.append(line.strip().split(","))
                found_task = False
            print("─" * 80 + "\n")
            for task in data:
                if task[5].strip() == "Yes":
                    found_task = True
                    print(f'''Task:                        {task[1]}
Assigned to:                  {task[0]}
Date assigned:               {task[3]}
Due date:                    {task[4]}
Task complete?               {task[5]}
Task description:
{task[2]}''')
                    print("\n" + "─" * 80 + "\n")
            if not found_task:
                print("You have no completed tasks.\n")
    except FileNotFoundError:
        print("File does not exist")


def delete_task():

    '''
    This code will open tasks.txt and read all tasks, delete the task a user
    chooses to delete then rewrite the file with the remaining tasks
    '''

    while True:
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                tasks = []
                for lines in file:
                    tasks.append(lines.strip().split(","))
                print("\nWhich task would you like to delete?")
                # get tasks with a relevant indexing number
                for task_no, line in enumerate(tasks, start=1):
                    print(f"{task_no}:{line[1]}...")
                choice = int(input("\nEnter the number of the task you'd like to delete: "))
                if choice >= 1 and choice <= len(tasks):
                    break
                else:
                    print("Try again. Enter a number from (1-3)")
                    continue
        except FileNotFoundError:
            print("File does not exist.")
        except ValueError:
            print("Invalid input. Enter a number from (1-3)")

    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            # Strip all leading/trailing whitespace and ignore blank lines
            data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("File does not exist.")
        data = []

    # Delete the selected line if it's valid
    if 1 <= choice <= len(data):
        del data[choice - 1]
    else:
        print("Invalid line number.")

    # rewrite the remaining lines
    if len(data) > 1:
        try:
            # used this method to avoid empty line issue after writing the new data
            with open("tasks.txt", "w", encoding="utf-8", newline="") as file:
                file.write(data[0])
                for row in data[1:]:
                    file.write("\n" + row)
                    print("Task deleted.")
        except FileNotFoundError:
            print("This file does not exist.")
    elif len(data) == 1:
        try:
            with open("tasks.txt", "w", encoding="utf-8", newline="") as file:
                file.write(data[0])
                print("Task deleted.")
        except FileNotFoundError:
            print("This file does not exist.")
    else:
        try:
            with open("tasks.txt", "w", encoding="utf-8", newline="") as file:
                file.write("")
                print("Task deleted. You have no active tasks left.")
        except FileNotFoundError:
            print("This file does not exist.")


def generate_reports():
    # Read and parse task data from tasks.txt
    try:
        with open("tasks.txt", "r", encoding="utf-8") as file:
            data = []
            for lines in file:
                line = [items.strip() for items in lines.split(",")]
                data.append(line)

    except FileNotFoundError:
        print("tasks.txt file cannot be found")

    # === TASK OVERVIEW REPORT ===

    total_tasks = len(data)
    tov_data_1 = f"total number of tasks: {total_tasks}"

    tasks_completed = 0
    for tasks in data:
        if tasks[5] == "Yes":
            tasks_completed += 1
    tov_data_2 = f"number of completed tasks: {tasks_completed}"

    tasks_uncompleted = 0
    for tasks in data:
        if tasks[5] == "No":
            tasks_uncompleted += 1
    tov_data_3 = f"number of uncompleted tasks: {tasks_uncompleted}"

    # Count how many uncompleted tasks are overdue
    overdue_tasks = 0
    for tasks in data:
        if tasks[5] == "No" and datetime.strptime(str(tasks[4]), "%d %b %Y") < datetime.now():
            overdue_tasks += 1
    tov_data_4 = f"number of overdue tasks: {overdue_tasks}"

    # Percentage of incomplete tasks
    incomplete_percentage = tasks_uncompleted/total_tasks*100
    tov_data_5 = f"percentage of incomplete tasks: {round(incomplete_percentage, 2)}%"

    # Percentage of overdue tasks
    overdue_percentage = overdue_tasks/total_tasks*100
    tov_data_6 = f"percentage of overdue tasks: {round(overdue_percentage, 2)}%"

    # Combine all task stats into a tuple
    task_overview_data = (tov_data_1, tov_data_2, tov_data_3, tov_data_4, tov_data_5, tov_data_6)

    # Write task overview report to fi
    with open("task_overview.txt", "w", encoding="utf-8", newline="") as file:
        file.write(str(task_overview_data[0]))  # First item directly
        for item in task_overview_data[1:]:
            file.write("\n" + str(item))  # Write each on a new line

    # === USER OVERVIEW REPORT ===

    # Read all users from user.txt
    with open("user.txt", "r", encoding="utf-8") as f:
        users = []
        for line in f:
            if line.strip():  # skip empty lines
                parts = line.strip().split(",")
                username = parts[0].strip()
                users.append(username)

    total_users = len(users)

    # --- Read tasks ---
    with open("tasks.txt", "r", encoding="utf-8") as f:
        tasks = []
        for line in f:
            if line.strip():
                task_data = [item.strip() for item in line.strip().split(",")]
                tasks.append(task_data)

    total_tasks = len(tasks)

    # --- Stats container ---
    user_stats = {}

    # --- For each user, calculate stats ---
    for user in users:
        # Get all tasks assigned to this user
        user_tasks = []
        for task in tasks:
            if task[0] == user:
                user_tasks.append(task)

        num_tasks = len(user_tasks)

        if num_tasks == 0:
            user_stats[user] = {
                "total": 0,
                "percent_assigned": 0,
                "percent_completed": 0,
                "percent_incomplete": 0,
                "percent_overdue": 0
            }
            continue

        # Count completed and overdue tasks
        completed = 0
        overdue = 0

        for task in user_tasks:
            is_complete = task[5].lower() == "yes"
            if is_complete:
                completed += 1
            else:
                due_date = datetime.strptime(task[4], "%d %b %Y").date()
                if due_date < datetime.today().date():
                    overdue += 1

        incomplete = num_tasks - completed

        user_stats[user] = {
            "total": num_tasks,
            "percent_assigned": round((num_tasks / total_tasks) * 100, 2),
            "percent_completed": round((completed / num_tasks) * 100, 2),
            "percent_incomplete": round((incomplete / num_tasks) * 100, 2),
            "percent_overdue": round((overdue / num_tasks) * 100, 2)
        }

    # --- Write to user_overview.txt ---
    with open("user_overview.txt", "w", encoding="utf-8") as file:
        file.write("===== USER OVERVIEW REPORT =====\n\n")

        # i. Total registered users
        file.write(f"Total number of users: {total_users}\n")

        # ii. Total number of tasks
        file.write(f"Total number of tasks: {total_tasks}\n\n")

        # iii. Detailed stats per user
        file.write("------ PER-USER STATISTICS ------\n\n")
        for user, stats in user_stats.items():
            file.write(f"User: {user}\n")
            file.write(f"  Total tasks assigned: {stats['total']}\n")
            file.write(f"  % of total tasks assigned: {stats['percent_assigned']}%\n")
            file.write(f"  % completed: {stats['percent_completed']}%\n")
            file.write(f"  % incomplete: {stats['percent_incomplete']}%\n")
            file.write(f"  % overdue and incomplete: {stats['percent_overdue']}%\n")
            file.write("-" * 40 + "\n")


def display_statistics():

    '''
    Reads the content of task_overview.txt and user_overview.txt files
    and displays them to the user.
    '''

    try:
        print("\n" + "=" * 30 + " TASK OVERVIEW " + "=" * 30)
        with open("task_overview.txt", "r", encoding="utf-8") as file:
            print(file.read())

        print("\n" + "=" * 30 + " USER OVERVIEW " + "=" * 30)
        with open("user_overview.txt", "r", encoding="utf-8") as file:
            print(file.read())

    except FileNotFoundError:
        print("One or both report files not found. Generate the reports first using the 'generate_reports()' function.")


# ==== Login Section ====
'''This code allows a user to login.
The code reads usernames and passwords from the user.txt file
The stores the usernames and passwords in a dictionary called users
Then uses a while loop to validate the user name and password.
'''
# creates a dictionary for users
users = {}
try:
    with open("user.txt", "r", encoding="utf-8") as file:
        for lines in file:
            # creates a list out of each line in the "user.txt" file
            # and removes whitespace. then assigns it variables.
            username, password = [item.strip() for item in lines.split(",")]
            # adds each users username and password to the dictionary
            users[username] = password
except FileNotFoundError:
    print("This file does not exist.")

while True:
    # Prompt user to enter username and password
    input_username = input("Enter your username: ")
    input_password = input("Enter your password: ")
    # checks if the username exists in user and if the password matches it
    if input_username in users and input_password == users[input_username]:
        print(f"\nWelcome {input_username}")
        break
    elif input_username not in users:
        print("Invalid username. Try again")
        continue
    else:
        print("Password does not match username. Try again")


# ---------menu for admin user--------- #

while True:
    if input_username == "admin":
        # Present the menu to the user and
        # make sure that the user input is converted to lower case.
        admin_menu = input(
            '''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
ds - display statistics
gr - generate reports
e - exit
: '''
        ).lower()
    else:
        break

    if admin_menu == 'r':
        reg_user(users)

    elif admin_menu == 'a':
        add_task(users)

    elif admin_menu == 'va':
        view_all()

    elif admin_menu == 'vm':
        view_mine(input_username)

    elif admin_menu == 'vc':
        view_completed()

    elif admin_menu == 'del':
        delete_task()

    elif admin_menu == 'ds':
        generate_reports()
        display_statistics()

    elif admin_menu == 'gr':
        generate_reports()

    elif admin_menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")


# ---------menu for regular users--------- #

while True:
    if input_username != "admin":
        # Present the menu to the user and
        # make sure that the user input is converted to lower case.
        menu = input(
            '''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
        ).lower()
    else:
        break
    if menu == 'a':
        add_task(users)

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(input_username)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
