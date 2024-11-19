# Installation Guide

1. Create python virtual environment

   ```bash
   python -m venv .venv
   ```

2. Install python package

   For MacOS run these command before follow below instruction

   Install [brew](https://brew.sh) then

   ```bash
   brew install mysql-client pkg-config
   ```

   For window / Linux user run just this command

   ```bash
   pip install -r requirements.txt
   ```

3. Install nodejs follows [instruction](https://nodejs.org/en/download/package-manager)

4. Get into frontend directory

   ```bash
   cd frontend
   ```

5. install js package

   ``` bash
   npm install
   ```

6. setup [frontend variable](./frontend/README.md#setup-variable)

7. Follow MySQL [installation & set up guide](./database_guide.md)

8. Migrate Django database

   ```bash
   python manage.py migrate
   ```

9. Setup google oauth by follow [Google oauth guide](./google_credentials_guide.md)