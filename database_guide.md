# PostgreSQL set up guide

## Using free online hosting database
1. Go to [render.com](https://render.com)
2. Create account and login
3. Go to [Create database instance](https://dashboard.render.com/new/database)
4. Fill information about database
5. Under Plan Options choose **Free** 

    _Note:_  free tier database on [render.com](https://render.com) will reset every 30 days
6. Click **Create Database**
7. Wait until service is ready
8. Go to [Render Dashboard](https://dashboard.render.com)
9. Select database that you have created before
10. Select Connect > External then copy External Database URL
11. Go to [environment file](backend/sample.env)
12. Set environment variable
    ```
    USE_URL=TRUE
    DATABASE_URL=<External Database URL that you have copy before>
    ```



