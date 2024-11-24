# Installation Guide


Follow these steps to set up **KU TangTee** project on your local machine.

### 1. Download the Code 
    
Clone the repository to your local directory using Git:

```bash
git clone https://github.com/OmegaOoh/ku-tangtee.git
```

### 2. Set Up a Python Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

### 3. Install Required Python Packages

**macOS**

Before proceeding, install [Homebrew](https://brew.sh) if you haven't already, then run:


   ```bash
   brew install mysql-client pkg-config
   ```

**Windows/Linux**

Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### 4. Install Node.js
Download and install Node.js from the [Node.js website](https://nodejs.org/en/download/package-manager). You may need to restart your device afterward.

### 5. Set Up Frontend Variables
Navigate to the Frontend Directory (`\ku-tangtee\frontend`):

   ```bash
   cd frontend
   ```
Then, follow the instructions in the [setup variable guide](./frontend/README.md#setup-variable).

### 6. Install & Set Up MySQL
Follow the instructions in the [MySQL installation and setup guide](./database_guide.md).

### 7. Migrate Django Database
Navigate to the Backend Directory (`\ku-tangtee\backend`):

   ```bash
   cd ..\backend
   ```

Then, run the following command to apply database migrations:

   ```bash
   python manage.py migrate
   ```

### 8. Set Up Google OAuth
Follow the instructions in the [Google credentials guide](./google_credentials_guide.md).
