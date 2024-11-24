# KU TangTee, Activities Hub for KU Student

[![codecov](https://codecov.io/gh/OmegaOoh/ku-tangtee/graph/badge.svg?token=3JS2AG5IFC)](https://codecov.io/gh/OmegaOoh/ku-tangtee) [![Lint JavaScript with JSHint](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jshint.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jshint.yml) [![Lint with flake8](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/flake8.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/flake8.yml)  [![Type check with mypy](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/mypy.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/mypy.yml) [![Run Jest Tests](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jest.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jest.yml) [![Run Django tests](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/coverage.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/coverage.yml)

Web applications powered by Django and VueJS to gather people for events or activities for KU students.

## Documents

The document regarding the development of this project can be found in the [wiki](../../wiki)

## How to run

**Prerequisite**: Install the app by following [Installation Guide](INSTALLATION.md)

Application needed to BOTH frontend and backend (two separate instances)

1. Activate Virtual Environment

      **macOS/Linux**

      ```bash
      source .venv/bin/activate
      ```
   
      **Windows**

      ```bash
      .venv\Scripts\activate
      ```

2. Backend Server
   1. Navigate to backend directory of the app (`\ku-tangtee\backend`)
   2. Run in Terminal

      ```bash
      python manage.py runserver
      ```

3. Frontend Server
   1. Navigate to frontend directory of the app (`\ku-tangtee\frontend`)
   2. Run in Terminal

      ``` bash
      npm run serve
      ```

4. Connect to site (Default Host is `127.0.0.1:8080`)

5. To stop the server, press CTRL-C in the terminal window. Then deactivate Virtual Environment:

      ``` bash
      deactivate
      ```