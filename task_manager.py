"""
CAPSTONE PROJECT III - task_manager.py: V2.00

This program is the complete version of the task manager program that can
add new users/tasks, edit/view the tasks, and generate the statistics
behind the tasks created by the user(s).

The user must login to gain access to the program first.

Once logged in, provide the user with menu options to perform the following:
    r - register a new unique user to the user.txt file
    a - add new user tasks to the tasks.txt file
    va - view all tasks from the tasks.txt file
    vm - view the tasks of the logged in user from the tasks.txt file
         edits the user's specific tasks and can mark them as complete
    gr - generates the task and user overview text files containing the
         generated statistics of the task information for each user.
    ds - display the total number of users and tasks in the program from
         the user.txt and tasks.txt files
    e - exit the program safely
"""
import datetime


def login():

    """
    Requests the user to login with their credentials before accessing the program
    :return: String username
    """
    # Open user text file to acquire all user credentials
    with open("user.txt", "r+") as file:
        information = file.readlines()

    valid_attempts = 3

    # Perform input validation of the user's credentials with valid attempts remaining
    while valid_attempts != 0:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        # Checks all of the known users in the text file to validate username and password
        for credentials in information:
            user_info = credentials.split(", ")
            user_info = "\n".join(user_info)
            user_info = user_info.split()

            # Return the user's username upon successful login
            if username in user_info and password == user_info[1]:
                print("Login successful!\n")
                return username

        # Requests the user to try again for failed login
        valid_attempts -= 1
        print("Invalid username or password! Please try again...\n")
    print("\nToo many invalid attempts!\nExiting program...")
    return None


# Calls login function before displaying the main menu
username = login()


def check_usernames():
    """
    Reads all of the usernames in the text file.

    :return: List of usernames in the text file
    """
    usernames = []
    with open("user.txt", "r+") as file:
        information = file.readlines()

    for credentials in information:
        user_info = credentials.split(", ")
        username = user_info[0]
        usernames.append(username)

    return usernames


def check_date(date):
    """
    Checks if the date format of the date string is valid

    :param date: String date of task
    :return: Boolean
    """
    try:
        if datetime.datetime.strptime(date, "%Y-%m-%d").date():
            return True
    except Exception:
        return False


def generate_report():
    """
    Generates the user and task overview text files from the user.txt and tasks.txt files

    :return:
    """

    usernames = check_usernames()

    # Dictionary stores each users total assigned tasks and
    # percentage of assigned complete, incomplete, and overdue tasks.
    user_information = {}

    # List stores all of the total, completed, incomplete, overdue tasks and
    # the percentage of the incomplete and overdue tasks.
    task_information = [0, 0, 0, 0, 0, 0]

    with open("tasks.txt", "r+") as read_file:
        tasks = read_file.readlines()

    # Stores total number of tasks in tasks.txt
    total_tasks = len(tasks)

    for user in usernames:

        # Declare 3 variables to store User's task information
        assigned_tasks = 0
        completed_tasks = 0
        incomplete_tasks = 0
        overdue_tasks = 0

        # Define new user value in dictionary
        user_information[user] = []

        for task in tasks:

            task = task.split(", ")

            # Adds total number of user's task
            if task[0] in user:
                assigned_tasks += 1

                # Add the total number of complete, incomplete, and overdue tasks
                if "No" in task[5]:
                    incomplete_tasks += 1

                if "Yes" in task[5]:
                    completed_tasks += 1

                if datetime.datetime.strptime(task[3], "%Y-%m-%d") < datetime.datetime.now() and "No" in task[5]:
                    overdue_tasks += 1

        # Prevent calculation errors from stoping the program
        try:
            if total_tasks == 0 or assigned_tasks == 0:
                assigned_percentage = 0.00
                completed_percentage = 0.00
                incomplete_percentage = 0.00
                overdue_percentage = 0.00

            else:
                assigned_percentage = round((assigned_tasks / total_tasks) * 100, 2)
                completed_percentage = round((completed_tasks / total_tasks) * 100, 2)
                incomplete_percentage = round((incomplete_tasks / total_tasks) * 100, 2)
                overdue_percentage = round((overdue_tasks / total_tasks) * 100, 2)

            user_information[user].append(assigned_tasks)
            user_information[user].append(assigned_percentage)
            user_information[user].append(completed_percentage)
            user_information[user].append(incomplete_percentage)
            user_information[user].append(overdue_percentage)

        except ZeroDivisionError:
            print("Division by 0 Calculation Found. Information Not Generated!")

    # Write each user's task information to user_overview.txt
    with open("user_overview.txt", "w") as write_file:

        for u in user_information:
            write_file.write(f"""User: {u}
            Assigned Tasks:             {user_information[u][0]}
            Assigned Task Percentage:   {user_information[u][1]}%
            Completed Task Percentage:  {user_information[u][2]}%
            Incomplete Task Percentage: {user_information[u][3]}%
            Overdue Task Percentage:    {user_information[u][4]}%
----------------------------------------------------------\n""")

    for task in tasks:

        task = task.split(", ")

        # Adds total number of user's task
        if task[0] in user:
            assigned_tasks += 1

        # Add the total number of complete, incomplete, and overdue tasks
        if "No" in task[5]:
            task_information[2] += 1

        if "Yes" in task[5]:
            task_information[1] += 1

        if datetime.datetime.strptime(task[3], "%Y-%m-%d") < datetime.datetime.now() and "No" in task[5]:
            task_information[3] += 1

    # Prevent calculation errors from stoping the program
    try:
        task_information[0] = total_tasks

        if task_information[0] == 0:
            task_information[4] = 0
            task_information[5] = 0
        else:
            task_information[4] = round((task_information[2] / task_information[0]) * 100, 2)
            task_information[5] = round((task_information[3] / task_information[0]) * 100, 2)

        # Write task information to task_overview.txt
        with open("task_overview.txt", "w") as write_file:
            write_file.write(f"""Total Number of Tasks: {task_information[0]}
Total Number of Completed Tasks: {task_information[1]}
Total Number of Incomplete Tasks: {task_information[2]}
Total Number of Overdue Tasks: {task_information[3]}
Percentage of Incomplete Tasks: {task_information[4]}%
Percentage of Overdue Tasks: {task_information[5]}%\n""")
    except ZeroDivisionError:
        print("Division by 0 Calculation Found. Information Not Generated!")

    print("Reports Generated!\n\n")


# Call the function to generate reports by default
generate_report()

# Allows user access to the program upon successful login
while username is not None:
    print(f"Welcome, {username}!\nDate: {datetime.datetime.today().date()}\n\n")

    # Displays menu options for admin user
    if username == "admin":
        # Request the user to choose a menu option
        menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate statistics
ds - display statistics 
e - exit
: ''').lower()

    # Displays menu options for non-admin users
    else:
        menu = input('''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
gr - generate statistics
e - exit
: ''').lower()

    # Registers new users to the program
    if menu == 'r' and username == "admin":
        with open("user.txt", "r+") as read_file:
            information = read_file.readlines()

        # Perform input validation to ensure that new users are regisered to the text file correctly
        while True:
            new_username = input("Please enter new username: ")
            new_password = input("Please enter new password: ")
            confirm_password = input("Please confirm new password: ")

            if new_username == "":
                print("Username cannot be empty. Please enter at least 1 character.\n")

            elif new_username in check_usernames():
                print("Username already exists! Please enter a unique username\n")

            elif new_password == "":
                print("Password cannot be empty. Please enter at least 1 character.\n")

            elif new_password != confirm_password:
                print("Passwords do not match! Please try again...\n")

            elif new_username != "" and new_password != "" and new_password == confirm_password:
                with open("user.txt", "a") as file:
                    file.writelines(f"\n{new_username}, {new_password}")
                print("\nRegistration Successful!\n")
                break

    # Adds new tasks to the program
    elif menu == 'a':
        assignee = input("Enter the username you are assigning the task to: ")
        title = input("Title: ")
        description = input("Description: ")
        due_date = input("Due Date (YYYY-MM-DD) | (i.e. 2024-06-20): ")
        current_date = datetime.datetime.today().date()
        task_status = "No"

        # Print warning message if user does not exist in the text file
        if assignee not in check_usernames():
            print("\nWARNING!\nUser does not exist!")

        # Checks if date is valid before writing it to the text file
        if check_date(due_date):

            with open("tasks.txt", "a") as write_file:
                write_file.writelines(f"\n{assignee}, {title}, {description}, {due_date}, {current_date}, {task_status}")

            print("Task Added!\n\n")

        else:
            print("Invalid Date Format! Please enter a valid due date!\n\n")

    # Prints all of the user tasks added to the program
    elif menu == 'va':
        with open("tasks.txt", "r+") as read_file:
            information = read_file.readlines()

        count = 1
        for task in information:
            task_info = task.split(", ")

            print("----------------------------------------")
            print(f"""Task #{count}
Assignee:       {task_info[0]}
Title:          {task_info[1]}
Description:    {task_info[2]}
Due Date:       {task_info[3]}
Assigned Date:  {task_info[4]}
Completed:      {task_info[5]}
""")
            count += 1
        print("----------------------------------------\n")

    # Prints all the tasks added to the program of the logged in user
    elif menu == 'vm':
        with open("tasks.txt", "r+") as read_file:
            information = read_file.readlines()

        user_tasks = {}
        count = 1

        for task in information:
            task_info = task.split(", ")

            if username == task_info[0]:

                user_tasks[count-1] = task_info

                print("----------------------------------------")
                print(f"""Task #{count}
Assignee:       {task_info[0]}
Title:          {task_info[1]}
Description:    {task_info[2]}
Due Date:       {task_info[3]}
Assigned Date:  {task_info[4]}
Completed:      {task_info[5]}
""")
            count += 1

        print("----------------------------------------\n")

        try:
            task_number = int(input("Choose a task number to edit or mark a task as complete: (Enter -1 to "
                                    "return to menu): "))

            if task_number == -1:
                print()

            elif (task_number - 1) in user_tasks:
                task_choice = int(input("Choose between 1 - 2:\n1. Mark as Complete\n2. Edit Task\n: "))

                # Marks the task complete
                if task_choice == 1 and "No" in user_tasks[task_number - 1][5]:
                    user_tasks[task_number - 1][5] = "Yes\n"
                    print("Task Completed!\n\n")

                elif task_choice == 1 and "Yes" in user_tasks[task_number - 1][5]:
                    print("Task Already Completed!\n\n")

                # Edits the task
                elif task_choice == 2 and "No" in user_tasks[task_number - 1][5]:
                    new_assignee = input("Enter a user to reassign this task to: (Leave Empty to Skip)"
                                         "\n: ")
                    new_due_date = input("Enter new due date of this task (YYYY-MM-DD): (Leave Empty to Skip)\n: ")

                    # Does not edit the task and returns to the menu
                    if new_assignee == "" and new_due_date == "":
                        print("Task Not Edited!!\n\n")

                    if new_due_date != "":

                        # Checks if the due date is valid before changing it
                        if check_date(new_due_date) == True:
                            user_tasks[task_number - 1][3] = new_due_date

                        else:
                            print("Invalid Date Format! Please enter a valid due date!\n\n")

                    if new_assignee != "":

                        # Checks if user exists before reassigning task
                        if new_assignee in check_usernames():
                            user_tasks[task_number - 1][0] = new_assignee

                        else:
                            print("Unable to reassign task! User does not exist!\n\n")

                    print("Task Edited Successfully!!\n\n")

                elif task_choice == 2 and "Yes" in user_tasks[task_number - 1][5]:
                    print("Cannot edit complete tasks. Please choose a different task.\n\n")

                else:
                    print("Invalid Option! Please choose between 1 - 2.\n\n")

            else:
                print("Invalid Choice!\nPlease select a valid task number!\n\n")

            count = 1

            # Update task information
            for task in information:
                for index in user_tasks:

                    if count == (index + 1):
                        task_info = ", ".join(user_tasks[index])

                        information[index] = task_info

                count += 1

            with open("tasks.txt", "w") as write_file:
                for task in information:
                    write_file.write(f"{task}")

        except IndexError:
            print("Task does not exist...\nPlease select an existing task number!\n\n")

        except ValueError:
            print("Invalid Choice!\nPlease select a valid task number!\n\n")

    # Generates the reports
    elif menu == 'gr':
        generate_report()

    # Prints the statistics of the users and tasks in the program
    elif menu == 'ds' and username == "admin":
        total_tasks = 0
        total_users = 0

        with open("tasks.txt", "r+") as read_file:
            total_tasks = len(read_file.readlines())

        with open("user.txt", "r+") as read_file:
            total_users = len(read_file.readlines())

        print("Total Number of Users:", total_users)

        with open("task_overview.txt", "r+") as read_file:
            task_overview = read_file.readlines()
            for line in task_overview:
                print(line)

        with open("user_overview.txt", "r+") as read_file:
            user_overview = read_file.readlines()
            for line in user_overview:
                print(line)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again\n")