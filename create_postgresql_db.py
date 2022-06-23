import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

# Returns the full path of the executing script
basedir = os.path.abspath(os.path.dirname(__file__))

# Add all environment variable definitions in the .env file to os.environ
load_dotenv()
DB_USERNAME = os.environ.get("FLASK_DB_USERNAME")
DB_PASSWORD = os.environ.get("FLASK_DB_PASSWORD")
DB_HOST = os.environ.get("FLASK_DB_HOST")


def get_databases():

    try:
        # Connect to an existing database server
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information:")
        print(connection.get_dsn_parameters(), "\n")
        # Execute SQL query to get PostgreSQL version
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print(f"You are connected to / {record}, \n")
        # Fetch all databases and print them
        print("Databases on Server: ")
        cursor.execute("SELECT datname FROM pg_database;")
        records = cursor.fetchall()
        for record in records:
            print(record)

    except(Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL {error}\n")

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("\nPostgreSQL connection is closed.\n")


def create_database():
    try:
        # Connect to an existing database server
        connection = psycopg2.connect(
            host="localhost",
            user=DB_USERNAME,
            password=DB_PASSWORD)

        # Open a cursor to perform database operations
        cursor = connection.cursor()

        # "CREATE DATABASE" requires automatic commits
        connection.autocommit = True
        # Create databases
        cursor.execute("CREATE DATABASE issue_tracker")
        cursor.execute("CREATE DATABASE test_db")
        connection.autocommit = False

        # Fetch all databases
        cursor.execute("SELECT datname FROM pg_database;")
        records = cursor.fetchall()
        for record in records:
            print(record)

        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        # Catch error if db already exists
        if e.pgcode == "42P04":
            print("\nNo new Database created, Database already exists!\n")
        else:
            print("Oops an error happened!\n")
            print(e.pgerror)
            print(e.pgcode)
            sys.exit(1)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.\n")


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


menu_options = {
    1: 'List available Databases',
    2: 'Create Database',
    0: 'Exit',
}


if __name__ == "__main__":
    # Print menue and catch exceptions
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('\nPlease enter option: '))
        except ValueError:
            print('Wrong input. Try again!\n')
        # Check input and call function
        if option == 1:
            get_databases()
        elif option == 2:
            create_database()
        elif option == 0:
            exit()
        else:
            print('Invalid option. Please choose between 0 and 2.')
