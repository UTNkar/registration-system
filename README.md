# registration-system

## Installation for mac and linux
1. Install Python 3
2. [Install postgresql](INSTALLING_POSTGRES.md)
2. Install the following packages:
  - python3-venv
  - python3-dev
  - build-essential
  - libpq-dev

3. Clone the repository
4. Copy the file `.env-template` and name the copy `.env`
5. Fill in the necessary variables in `.env`
6. Run `source source_me.sh`
7. Run `pip install --upgrade pip` to make sure that pip is running the latest version
8. Run `pip install -r dev-requirements.txt`
9. Use `cd registrationSystem` to enter the website directory
10. Run `./manage.py migrate` to setup the database structure
11. Run `./manage.py createsuperuser` to add a new admin user
12. Run `./manage.py runserver` to start your local server

You can now visit `localhost:8000` and login with the user created in the previous steps

**IMPORTANT** When running any command, you must be in the virtual envionment (a.k.a `source source_me.sh`), the console should say (venv). To leave the virtual environment, run `deactivate`.
