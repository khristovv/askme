## Setting up askme with PostgreSQL
1. Installing PosgreSQL and all required dependencies

    - sudo apt-get install postgresql postgresql-contrib
    - sudo apt-get install libpq-dev python3.8-dev
    - pip install -r requirements.txt

    **NOTE: psycopg2 is the adapter we're using to connect to Postgres and it's dependent on libpq-dev and python3.8-dev. It's located in requirements.txt
    so installing of all packages must happen last !**

2. Start the server if not started automatically

    - sudo /etc/init.d/postgresql start

3. Configure database and user

    3.1 Enter Postgres terminal
    - sudo -u postgres psql 
    
    3.2 Create database and user - other name and password could be provided BUT make sure to also set them as env variables
    USER maps to ASKME_DB_ADMIN env variable; PASSWORD maps to ASKME_DB_ADMIN_PASS env variable
    - `CREATE DATABASE askmedb;`
    - `CREATE USER {name} WITH ENCRYPTED PASSWORD {password}';`
    
    3.3 Modify connection parameters (as recommended by official Django docs)
    - `ALTER ROLE {name} SET client_encoding TO 'utf8';`
    - `ALTER ROLE {name} SET default_transaction_isolation TO 'read committed';`
    - `ALTER ROLE {name} SET timezone TO 'UTC';`
    
    3.4 Give user privileges
    - `GRANT ALL PRIVILEGES ON DATABASE askmedb TO {name};`
    - `ALTER USER {name} CREATEDB;`

4. Export env variables
For security reasons and good practices, the name and password of the created PostgreSQL user that is administrating
the project's database is not hardcoded in the `setttings.py` file, but we get them form the envirionemt variables
    - export ASKME_DB_ADMIN={same name used in step 3.2}
    - export ASKME_DB_ADMIN_PASS={same password used in step 3.2}

5. Run all migrations (env must be activated by this point)
    - `python manage.py migrate`

6. Create a super user to be able to login and acces the admin panel
    - `python manage.py createsuperuser`

7. Run the debug server
    - `python manage.py runserver`

