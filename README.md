# registration-system

## Installation
1. Install Python 3
2. Install python3-venv
3. Clone the repository
4. Run `source source_me.sh`
5. Run `pip install --upgrade pip` to make sure that pip is running the latest version
6. Run `pip install -r requirements.txt`
7. Use `cd registrationSystem` to enter the website directory
8. Run `./manage.py migrate` to setup the database structure
9. Run `./manage.py createsuperuser` to add a new admin user
10. Run `./manage.py runserver` to start your local server

You can now visit `localhost:8000` and login with the user created in the previous steps

**IMPORTANT** When running any command, you must be in the virtual envionment (a.k.a `source source_me.sh`), the console should say (venv). To leave the virtual environment, run `deactivate`.