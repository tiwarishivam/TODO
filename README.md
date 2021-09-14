# TODO
Todo app for managing tasks

Basic TODO app built using Django Rest Framework and default sqlite database.
DRF APIs for create, get, update and delete todo tasks.
Implemented Redis Caching.

APIs available:

1. api-token-auth/  # for getting auth token
2. /todo/get-task-list/  # for fetching all todo task for a paticular user
3. /todo/get-task/  # for fetching one todo task details
4. update-task/<task id>/  # for updating any todo task
5. create-task/  # for creating new todo task
6. delete-task/<task id>/  # for deleting any todo task

Follow the steps to runs it on development environment

Python version > 3 required

1. apt-get update -y

2. sudo apt-get install -y python3-venv

3. python3 -m venv todo-env

4. mkdir todo-proj

5. cd todo-proj/

6. source todo-env/bin/activate

7. Clone the repository

8. cd todoapp/

9. install all dependencies using:
    - pip install -r requiremtns.txt

10. run the following comand for creating all tables in the database:
    - python manage.py migrate

11. install Redis and run it on linux following the installation instruction in the link:
    - https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

12. python manage.py runserver
    server running on http://localhost:8000/


Future Scope:

1. Implement proper interactive UI for the TODO app.
2. Containerize the app using Docker.
