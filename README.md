# KU TangTee, Activities Hub for KU Student

[![codecov](https://codecov.io/gh/OmegaOoh/ku-tangtee/graph/badge.svg?token=3JS2AG5IFC)](https://codecov.io/gh/OmegaOoh/ku-tangtee) [![Lint with flake8](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/flake8.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/flake8.yml) [![Type check with mypy](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/mypy.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/mypy.yml) [![Lint JavaScript with JSHint](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jshint.yml/badge.svg)](https://github.com/OmegaOoh/ku-tangtee/actions/workflows/jshint.yml)

Web applications powered by Django and VueJS to gather people for events or activities for KU students.

## Documents

The document regarding the development of this project can be found in the [wiki](../../wiki)

## How to run

**Prerequisite**: Install the app by following [Installation Guide](INSTALLATION.md)

Application needed to BOTH frontend and backend (two separate instances)

1. Backend Server
   1. At the root directory of the app
   2. Run

      ```bash
      python manage.py runserver
      ```

2. Frontend Server
   1. Go Inside frontend directory of the app
   2. Run

      ``` bash
      npm run serve
      ```

3. Connect to site (Default Host is `127.0.0.1:8080`)
