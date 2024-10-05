# KU TangTee, Activities Hub for KU Student
web application for gathering people for events or activities powered by Django

## How to install
1. Create python virtual environment
   ```bash
   python -m venv .venv
   ```
2. Install python package
   ```bash
   pip install -r requirements.txt
   ```
3. Install nodejs follows [instruction](https://nodejs.org/en/download/package-manager)
4. Install vue 
   ```bash
   npm install -g @vue/cli
   ```
5. Follow MySQL [installation & set up guide](./database_guide.md)
6. Migrate Django database
   ```bash
   python manage.py migrate
   ```

## How to run
1. go in frontend directory 
   ```bash
   cd frontend
   ```
2. run frontend server
   ```bash
   npm run serve
   ```
3. get back to apps directory 
   ```bash
   cd ..
   ```
4. run backend server
   ```bash
   python manage.py runserver
   ```
5. Connect to site (Default Host is `localhost:8080`)


The document regarding the development of this project can be found in the project [wiki](../../wiki)
