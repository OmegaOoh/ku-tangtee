# MySQL installation & set up guide

## Install MySQL
1. Follow [this](https://dev.mysql.com/downloads/mysql/) link.
2. Select you operating system.
3. Download installer file.
4. Run the installer file.
5. Follow installer instruction.
6. Enter a password for root user when installer prompt.

## Set up a database
1. Login to MySQL terminal as a root user.

    ```
    mysql -u root -p
    ```

    After execute command, enter root password that you've set before in installer. 

2. Inside MySQL terminal, create a database for storing a data.

    ```sql
    CREATE DATABASE myDB;
    ```

    myDB can be any valid database name.

## (Optional) Create a user to access database instead of root.
1. Create user.

    ```sql
    CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
    ```

    user can be any valid username. password will be a key to identify this user

2. Grant necessary privileges to user on database.

    ```sql
    GRANT ALL PRIVILEGES ON myDB TO 'user'@'localhost';
    GRANT CREATE ON myDB TO 'user'@'localhost';
    ```

## Configure environments.
1. In [sample.env](./sample.env)
    ```
    # MySQL configuration
    DATABASE_NAME=myDB
    DATABASE_USER=root
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=3306
    ```
    Replace myDB with name of database that you has created before.

    Replace root with username if you have created a new user.

    Replace password with root password or user password if you have created a new user.


