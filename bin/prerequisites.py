#!/usr/bin/python
# -*- coding:utf8 -*
from lib.schema import *
import os
import argparse
import subprocess
import requests
import platform
import subprocess
import platform
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import subprocess
from typing import Dict, List, Optional, Any

"""
    prerequisites.py

    This script checks the prerequisites for execution of a WEB application.

    It checks the following:
    - the environment variables are set
    - apache is up and running
    - the database is available
    - the database is accessible by the default user
    - The schema has been defined
    - And minimal test data exist

    The scripts uses the following environment variables:
    - META_DB_HOST: the host name of the MySql server
    - META_DB_PORT: the port number of the MySql server
    - META_DB_USER: the user name to connect to the MySql server
    - META_DB_PASSWORD: the password to connect to the MySql server
    - META_DB_NAME: the name of the database to analyze

"""

class MySQLNotRunningError(Exception):
    """Custom exception for when MySQL is not running."""
    pass

class ApacheNotRunningError(Exception):
    """Custom exception for when Apache is not running."""
    pass

def parse_environment() -> Dict[str, Any]:
    """
    Analyze the environment variables and parse the command line arguments. Checks that mandatory parameters are set. returns a dictionary with the command line arguments and values from the environment.

    The following parameters can be set:
    - verbose: verbose mode
    - database: the database name
    - user: the user name to connect to the MySql server
    - password: the password to connect to the MySql server (optional)
    - urls: one or more URLs (multiple occurrences are possible)
    - create_db: boolean to create the databases if they do not exist (default: False)
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Parse environment variables and command line arguments")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-d", "--database", help="Database name")
    parser.add_argument("-u", "--user", help="User name for MySQL server")
    parser.add_argument("-p", "--password", help="Password for MySQL server (optional)")
    parser.add_argument("--urls", action="append", help="URLs (multiple occurrences are possible)")
    parser.add_argument("--databases", action="append", help="Databases (multiple occurrences are possible)")
    parser.add_argument("--create_db", action="store_true", default=False, help="Create databases if they do not exist")

    # Parse command line arguments
    args = parser.parse_args()

    # Create a dictionary to store the final configuration
    config: Dict[str, Any] = {}

    # Process each parameter
    config['verbose'] = args.verbose or os.environ.get('VERBOSE', '').lower() == 'true'
    config['database'] = args.database or os.environ.get('META_DB')
    config['user'] = args.user or os.environ.get('META_DB_USER')
    config['password'] = args.password or os.environ.get('META_DB_PASSWORD')
    config['urls'] = args.urls or os.environ.get('URLS', '').split(',') 
    config['databases'] = args.databases or os.environ.get('databases', '').split(',') 
    config['create_db'] = args.create_db

    # Check for mandatory parameters
    mandatory_params = ['database', 'user']
    missing_params = [param for param in mandatory_params if not config[param]]

    if missing_params:
        print(f"Missing mandatory parameters: {', '.join(missing_params)}")
        exit(1)

    return config

def check_apache() -> None:
    """
    Check if Apache is running.

    Raises:
    ApacheNotRunningError: If Apache is not running.
    """
    system = platform.system().lower()

    # Check if Apache process is running
    if system in ["linux", "darwin"]:  # Linux or macOS
        try:
            output = subprocess.check_output(["pgrep", "-f", "apache2|httpd"])
            if output:
                return  # Apache is running
        except subprocess.CalledProcessError:
            pass
    elif system == "windows":
        try:
            # Use 'cp1252' encoding for Windows
            output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq httpd.exe"], encoding='cp1252')
            if "httpd.exe" in output:
                return  # Apache is running
        except subprocess.CalledProcessError:
            pass

    # If process check fails, try making an HTTP request
    try:
        response = requests.get("http://localhost", timeout=5)
        if response.status_code == 200:
            return  # Apache is running
    except requests.RequestException:
        pass

    # If we've reached this point, Apache is not running
    print("Apache is not running")
    exit(1)

def check_mysql(host: str = 'localhost', user: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Check if MySQL is running.

    Args:
    host (str): The MySQL server host. Defaults to 'localhost'.
    user (str): The MySQL user. If None, only process-based check will be performed.
    password (str): The MySQL password. If None, only process-based check will be performed.

    Raises:
    MySQLNotRunningError: If MySQL is not running.
    """
    system = platform.system().lower()

    # Check if MySQL process is running
    if system in ["linux", "darwin"]:  # Linux or macOS
        try:
            output = subprocess.check_output(["pgrep", "-f", "mysqld"])
            if output:
                return  # MySQL is running
        except subprocess.CalledProcessError:
            pass
    elif system == "windows":
        try:
            output = subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq mysqld.exe"], encoding='cp1252')
            if "mysqld.exe" in output:
                return  # MySQL is running
        except subprocess.CalledProcessError:
            pass

    # If process check fails and credentials are provided, try making a MySQL connection
    if user is not None and password is not None:
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                connect_timeout=5
            )
            conn.close()
            return  # MySQL is running and we could connect
        except mysql.connector.Error:
            pass

    # If we've reached this point, MySQL is not running or we couldn't connect
    print("MySQL is not running or connection failed")
    exit(1)

def check_urls(urls: List[str], timeout: int = 5, max_workers: int = 10) -> Dict[str, str]:
    """
    Check if a list of URLs is reachable on a local server.

    Args:
    urls (list): A list of URLs to check.
    timeout (int): The timeout for each request in seconds. Default is 5.
    max_workers (int): The maximum number of threads to use. Default is 10.

    Returns:
    dict: A dictionary with URLs as keys and their status as values.
    """
    results: Dict[str, str] = {}

    def check_url(url: str) -> tuple[str, str]:
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = f"http://{url}"
            
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return url, "Reachable"
            else:
                return url, f"Not reachable (Status code: {response.status_code})"
        except requests.RequestException as e:
            return url, f"Error: {str(e)}"

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            url, status = future.result()
            results[url] = status

    return results

def check_php_version() -> str:
    """
    Returns the PHP version of the default PHP installation.
    """
    try:
        # Run the 'php -v' command and capture its output
        result = subprocess.run(['php', '-v'], capture_output=True, text=True, check=True)
        
        # Extract the version from the output
        version_line = result.stdout.split('\n')[0]
        version = version_line.split()[1]
        
        return version
    except subprocess.CalledProcessError:
        return "PHP is not installed or not in the system PATH"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def check_databases_exist(host: str, user: str, password: str, databases: List[str]) -> Dict[str, bool]:
    """
    Check if one or several MySQL databases exist.

    Args:
    host (str): MySQL server host
    user (str): MySQL user
    password (str): MySQL password
    databases (list): List of database names to check

    Returns:
    dict: A dictionary with database names as keys and boolean values indicating existence
    """
    results: Dict[str, bool] = {}

    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Get all existing databases
        cursor.execute("SHOW DATABASES")
        existing_databases = [db[0] for db in cursor.fetchall()]

        # Check each database
        for db in databases:
            results[db] = db in existing_databases

    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL server: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return results

def create_database(host: str, user: str, password: str, database_name: str) -> None:
    """
    Create a MySQL database.
    """
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Create the database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        print(f"Database '{database_name}' created.")

    except mysql.connector.Error as error:
        print(f"Error creating database: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#######################################################################
print ("Check Prerequisites to run a WEB application locally")

config = parse_environment()
if config['verbose']: print ("Configuration:", config)

check_apache()
print ("Apache is running")

check_mysql(host='localhost', user=config['user'], password=config['password'])
print ("MySql is running")

results = check_urls(config['urls'])
print("URL:", results)

php_version = check_php_version()
print(f"Current PHP version: {php_version}")

host = "localhost"
user = "root"
password = ""
databases_to_check = ["mysql", "information_schema", "nonexistent_db", "multi"]

existence_results = check_databases_exist(host, user, password, config['databases'])

for db, exists in existence_results.items():
    if exists:
        print(f"Database '{db}': Exists")
    else:
        if config['create_db']:
            create_database(host, user, password, db)
        else:
            print(f"Database '{db}': Does not exist")

print ("bye ...")