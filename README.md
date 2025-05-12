# Task_Manager (version 1.5 Flask: No Database)

## Table of Contents
- [Description](#description)
- [Intallation](#installation)
- [Usage](#usage)
- [Credits](#credits)

## Description
This version of the Python Capstone project will demonstrate my Task Manager simulation using the Flask Web Framework without any databases. Only text files (like the terminal version) will be used. 

## Installation
To install this project on your computer, you can run the following commands:
1. Create a directory (folder) where you wish to install the project.
2. Open your terminal/command prompt and navigate to the selected directory
3. In this directory, type the following command:
     ```sh
     git clone https://github.com/C-CREAD/Task_Manager
     ```
4. Navigate to the project folder inside the directory from above:
     ```sh
     cd (folder)
     ```
5. Create a virtual environment:
     ```sh
     python -m venv .venv
     ```
6. Install the required packages:
     ```sh
     pip install -r requirements.txt
     ```
7. Run the program using the following command:
     ```sh
     python task_manager.py 
     ```

### Docker
The docker repository containing the image can be found [here](https://hub.docker.com/repository/docker/ccread/task_manager/tags/flask/sha256:52fd124c14c06f96a5ccf1f62c9537314af07b1cee81047600ef8b73e262a393)
To run the Dockerfile of this project, make sure that you have Docker Desktop installed on your computer before proceeding, or you can try to run the project on Docker Playground [here](https://labs.play-with-docker.com/). 

#### Docker Desktop
Once Docker Desktop is installed, follow the instructions below:
1. Create a directory (folder_name) where you wish to install the project.
2. Open your terminal/command prompt and navigate to the selected directory
3. In the directory, type the following command to pull the image from the repository:
     ```sh
     docker pull ccread/task_manager:flask
     ```
4. Run the Docker image:
     ```sh
     docker run -d -p 3000:3000 ccread/task_manager:flask
     ```
   In your Docker Desktop, you will see the container of the image running. Click on the port 3000:3000 to be redirected to your browser or you can still go to your browser and enter this link:
     ```
     http://localhost:3000/
     ```.

#### Docker Playground
1. To pull the docker image:
     ```sh
     docker pull ccread/task_manager:flask
     ```
     ![image](https://github.com/user-attachments/assets/67f04e53-86f6-4dbf-ae51-fdf064eaf74b)
     ![image](https://github.com/user-attachments/assets/cd1b847c-40fe-4999-a3e1-ef86ee6abe85)
2. Run the Docker image and then click on the opened port: 3000:
     ```sh
     docker run -d -p 3000:3000 ccread/task_manager:flask
     ```
     ![image](https://github.com/user-attachments/assets/064a8f6a-a82d-4e9f-a49c-0c3ecc352d3e)

   NOTE: If you don't see a port opened, click on the "Open Port" button and enter 3000 in the prompt given by your browser. 

3. You should be redirected to a new tab with the image running the project.
     ![image](https://github.com/user-attachments/assets/78c4c3fc-5f6d-4384-a259-086321f14671)


## Usage
The user will be required to login to the project before accessing the menu options. For newcomers, the default admin credentials are:
```sh
Username: admin
Password: adm1n
```

### Register a User (admin only!)
This option will register new unique users into the program by entering their username and password.
This option is admin-only and cannot be accessed by non-admin users!

### Add Task
This option will add new tasks for users to complete by a certain due date. 

### View All Tasks
This option displays the task details for all users in the program.

### View My Tasks
This option displays the task details for the user logged in to the program and then requests the user to either mark the task as complete or edit the task by changing the assignee of the user or the due date of the task. 

### View Statistics (admin only!)
This option will generate the statistics of all the users and tasks, store them in new text files 'user_overview.txt' and 'task_overview.txt', and display the results on the web page.



## Credits
Shingai Dzinotyiweyi [GitHub Profile](https://github.com/C-CREAD)

[Repository Link:]([https://github.com/C-CREAD/Task_Manager](https://github.com/C-CREAD/Task_Manager/tree/flask_v1.5)) 

