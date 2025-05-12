"""
CAPSTONE PROJECT III - task_manager.py: V2.5 (No Database)

This project is the complete version of the task manager v2.0 with the Flask Web Framework implemented.

NOTE: To keep things simpler, there will not be any databases used as this project will continue to use
text files that were part of the v2.0. Databases will only be introduced in future versions of this project
(perhaps in v3.0).
"""
import os
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import secrets

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store permanent session data for 5 minutes
app.permanent_session_lifetime = timedelta(minutes=10)


def check_usernames():
    """
    Reads all of the usernames in the text file.

    :return: List of usernames in the text file
    """
    usernames = []
    with open("data/user.txt", "r+") as file:
        information = file.readlines()

    for credentials in information:
        user_info = credentials.split(", ")
        username = user_info[0]
        usernames.append(username)

    return usernames


def check_date(date):
    """
    Checks if the date format of the date string is valid
    """
    try:
        if datetime.strptime(date, "%Y-%m-%d").date():
            return True
    except Exception:
        return False


def get_user_tasks(username):
    """
    Get all tasks allocated to specific user and display in terminal
    """
    user_tasks = []

    with open("data/tasks.txt", "r+") as read_file:
        information = read_file.readlines()

        index = 0

        for task in information:
            task_info = task.strip().split(", ")
            task_info.append(index)     # Add index of each task
            if username == task_info[0]:
                user_tasks.append(task_info)
            index += 1
            #     print("----------------------------------------")
            #     print(f"""Task #{count}
            #         Assignee:       {task_info[0]}
            #         Title:          {task_info[1]}
            #         Description:    {task_info[2]}
            #         Due Date:       {task_info[3]}
            #         Assigned Date:  {task_info[4]}
            #         Completed:      {task_info[5]}
            #         """)
            # count += 1
            #
            # print("----------------------------------------\n")

    return user_tasks


def get_all_tasks():
    """
    Get all tasks (allocated to any user) and display in terminal
    """
    user_tasks = []

    with open("data/tasks.txt", "r+") as read_file:
        information = read_file.readlines()

        index = 0

        for task in information:
            task_info = task.strip().split(", ")
            task_info.append(index)
            user_tasks.append(task_info)

            # print("----------------------------------------")
            # print(f"""Task #{index+1}
            #     Assignee:       {task_info[0]}
            #     Title:          {task_info[1]}
            #     Description:    {task_info[2]}
            #     Due Date:       {task_info[3]}
            #     Assigned Date:  {task_info[4]}
            #     Completed:      {task_info[5]}
            #     """)
            index += 1

        # print("----------------------------------------\n")

    return user_tasks


def generate_reports():
    """
    Generates the user and task overview text files from the user.txt and tasks.txt files
    """

    usernames = check_usernames()

    # Dictionary stores each users total assigned tasks and
    # percentage of assigned complete, incomplete, and overdue tasks.
    user_information = {}

    # List stores all of the total, completed, incomplete, overdue tasks and
    # the percentage of the complete, incomplete and overdue tasks.
    task_information = [0, 0, 0, 0, 0, 0, 0]

    with open("data/tasks.txt", "r+") as read_file:
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

                if datetime.strptime(task[3], "%Y-%m-%d") < datetime.now() and "No" in task[5]:
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
    with open("data/user_overview.txt", "w") as write_file:

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

        if datetime.strptime(task[3], "%Y-%m-%d") < datetime.now() and "No" in task[5]:
            task_information[3] += 1

    # Prevent calculation errors from stoping the program
    try:
        task_information[0] = total_tasks

        if task_information[0] == 0:
            task_information[4] = 0
            task_information[5] = 0
            task_information[6] = 0
        else:
            task_information[4] = round((task_information[1] / task_information[0]) * 100, 2)
            task_information[5] = round((task_information[2] / task_information[0]) * 100, 2)
            task_information[6] = round((task_information[3] / task_information[0]) * 100, 2)

        # Write task information to task_overview.txt
        with open("data/task_overview.txt", "w") as write_file:
            write_file.write(f"""Total Number of Tasks: {task_information[0]}
Total Number of Completed Tasks: {task_information[1]}
Total Number of Incomplete Tasks: {task_information[2]}
Total Number of Overdue Tasks: {task_information[3]}
Percentage of Complete Tasks: {task_information[4]}%
Percentage of Incomplete Tasks: {task_information[5]}%
Percentage of Overdue Tasks: {task_information[6]}%\n""")
    except ZeroDivisionError:
        print("Division by 0 Calculation Found. Information Not Generated!")

    # print("Reports Generated!")

    return task_information, user_information


@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Requests the user to login with their credentials before accessing the program
    """

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Open user text file to acquire all user credentials
        with open("data/user.txt", "r+") as file:
            information = file.readlines()

        # Checks all of the known users in the text file to validate username and password
        for credentials in information:
            user_info = credentials.split(", ")
            user_info = "\n".join(user_info)
            user_info = user_info.split()

            # Return the user's username upon successful login
            if username in user_info and check_password_hash(user_info[1], password):
                flash("Login successful.", "success")
                session.permanent = True
                session["username"] = username
                return redirect(url_for("dashboard", username=username))

        # Return error message for invalid credentials
        flash("Invalid Credentials!", "danger")
        return redirect(url_for("login"))

    else:
        # Check if user is logged in
        if "username" in session:
            flash("User already logged in.", "info")
            return redirect(url_for("user"))

        return render_template("authentication/login.html")


@app.route("/logout")
def logout():
    """
    Logs the user out of the session
    """

    session.pop("username", None)
    flash("You have logged out successfully.", 'info')
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Requests the user to enter new credentials before logging in to access the program
    """

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Verify if new user is valid
        if username not in check_usernames() and password == confirm_password:
            with open("data/user.txt", "a") as file:
                file.writelines(f"\n{username}, {generate_password_hash(confirm_password)}")
            flash("User registered successfully.", 'success')
            return redirect(url_for("dashboard"))

        elif username in check_usernames():
            flash("User already exists! Try entering a different username.", "danger")

        elif password != confirm_password:
            flash("Passwords don't match! Please try again.", "danger")

        return render_template("authentication/register.html")

    else:
        if "username" not in session or session["username"] != "admin":
            flash("You do not have permission to access this page!", "danger")
            return redirect(url_for("user"))

        return render_template("authentication/register.html")


@app.route("/dashboard")
def dashboard():
    """
    Renders the dashboard page to display the user's task information
    """
    if "username" not in session:
        flash("Session has expired. Login Required.", "info")
        return redirect(url_for("login"))

    return render_template('dashboard.html', username=session["username"],
                           current_date=datetime.now().strftime('%A, %B %d, %Y'))


@app.route("/add_task", methods=["POST", "GET"])
def add_task():
    """
    Renders the page to add new tasks
    """

    if "username" not in session:
        flash("Session has expired. Login Required.", "info")
        return redirect(url_for("login"))

    if request.method == "POST":
        assignee = request.form["assignee"]
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        current_date = datetime.today().date().strftime("%Y-%m-%d")
        task_status = "No"

        if assignee not in check_usernames():
            flash("Assignee (user) does not exist!", "danger")

        elif not check_date(due_date):
            flash("Invalid date format. Must use (YYYY-MM-DD)", "danger")

        else:

            # Format Title and Description values
            title = title.replace(",", " ")
            description = description.replace(",", " ")

            with open("data/tasks.txt", "a") as write_file:
                write_file.write(f"{assignee}, {title}, {description}, {due_date}, {current_date}, {task_status}\n")

            flash("Task added successfully.", "success")
            return redirect(url_for("dashboard"))

    return render_template("add_task.html", users=check_usernames())


@app.route("/view_tasks")
def view_tasks():
    """
    Renders the page to view all tasks created.
    """
    if "username" not in session:
        flash("Session has expired. Login Required.", "info")
        return redirect(url_for("login"))

    tasks = get_all_tasks()

    if len(tasks) == 0:
        flash("No tasks created.", "info")
    return render_template("view_tasks.html", tasks=tasks)


@app.route("/my_tasks")
def my_tasks():
    """
    Renders the page to view all the user's tasks created.
    """
    if "username" not in session:
        flash("Session has expired. Login Required.", "info")
        return redirect(url_for("login"))

    tasks = get_user_tasks(session["username"])
    if len(tasks) == 0:
        flash("No tasks created.", "info")

    return render_template("my_tasks.html", tasks=tasks)


@app.route("/edit_task/<int:task_id>", methods=["POST", "GET"])
def edit_task(task_id):
    """
    Renders the page to let the user edit their selected task.
    """
    if "username" not in session:
        flash("Session has expired. Login Required.", "info")
        return redirect(url_for("login"))

    tasks = get_user_tasks(session["username"])

    # Check if the task selected is valid
    if task_id < 0 or task_id >= len(tasks):
        flash("Invalid Task ID", "danger")
        return redirect(url_for("my_tasks"))

    task = tasks[task_id]
    index = task[-1]

    if request.method == "POST":
        mark_complete = request.form.get("mark_complete") == "on"
        new_assignee = request.form["new_assignee"]
        new_due_date = request.form["new_due_date"]

        if new_assignee == "Keep current assignee":
            new_assignee = session["username"]

        task[0] = new_assignee
        task[3] = new_due_date

        if mark_complete:
            task[5] = "Yes"
        else:
            task[5] = "No"

        tasks = get_all_tasks()
        tasks[index] = task

        with open("data/tasks.txt", "w+") as write_file:
            for task in tasks:
                write_file.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}, {task[4]}, {task[5]}\n")

        flash("Task updated successfully.", "success")
        return redirect(url_for("my_tasks"))

    return render_template("edit_task.html", task=task, task_id=task_id, users=check_usernames())


@app.route("/statistics")
def statistics():
    """
    Renders the page to view all statistics about the tasks.
    """

    if "username" not in session or session["username"] != "admin":
        flash("You do not have permission to access this page!", "danger")
        return redirect(url_for("dashboard"))

    task_information, user_information = generate_reports()

    return render_template("statistics.html", task_information=task_information,
                           user_information=user_information)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(3000))