# Installation Guide

Download the code to a local directory.    
(One possible method is using ```git clone https://github.com/OmegaOoh/ku-tangtee.git```).  
       
Once done, do the following in the directory where you placed the project files. (Initially, "ku-tangtee")
1. Create python virtual environment

   ```bash
   python -m venv .venv
   ```

2. Install python package

   For macOS run these command before follow below instruction

   Install [brew](https://brew.sh) then

   ```bash
   brew install mysql-client pkg-config
   ```

   For window / Linux user run just this command

   ```bash
   pip install -r requirements.txt
   ```

3. [Install](https://nodejs.org/en/download/package-manager) node.js (May have to restart your device afterward)

4. Get into frontend directory (`\ku-tangtee\frontend`)

   ```bash
   cd frontend
   ```

5. [Setup](./frontend/README.md#setup-variable) frontend variable

6. [Install & Set up](./database_guide.md) MySQL

7. Navigate back to the root directory (`\ku-tangtee`)
   ```bash
   cd ..
   ```
8. Migrate Django database

   ```bash
   python manage.py migrate
   ```

9. [Setup](./google_credentials_guide.md) Google oauth