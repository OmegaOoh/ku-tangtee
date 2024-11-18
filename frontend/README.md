# frontend

## Setup Variable

1. Copy `sample.env` to `.env`
2. Add your [Google Client ID](../google_credentials_guide.md) to `VUE_APP_GOOGLE_CLIENT_ID`
3. Add your Django Base URL to `VUE_APP_BASE_URL` (The Domain must be the same with frontend to prevent authentication works correctly)
   for examples: if you are using `localhost:8080` to connect to frontend, `VUE_APP_BASE_URL` need to be `localhost:8000`

## Project setup

In frontend directory (`\ku-tangtee\frontend`)

### Install js package

```sh
npm install
```

### Run frontend server

```sh
npm run serve
```
