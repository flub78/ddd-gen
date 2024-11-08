#!/usr/bin/python
# -*- coding:utf8 -*
from lib.schema import *
import os
import importlib.util
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
from configloader import ConfigLoader
import textwrap

"""
    prerequisites.py

    This script checks the prerequisites for execution of a WEB application.

    It checks the following:
    - apache is up and running
    - the MySQL is accessible by the root user
    - the correct PHP version is installed

    Then it checks that we have some specific environments:
    - databases
    - database schema
    - database user and password
    - The schemas are defined, some tables exist
    - Specific amount of data is inserted in the database
    - Specific values are inserted in the database


    Syntax:
    python prerequisites.py --config config.py

    All the things to checks are described into a python configuration file (setenv.py) by default.
    The parameters recognized by prerequisites.py only define what to do when the prerequisites defined in the file are not met.

    It is voluntary to keep a written definition of the prerequisites. It makes things easier
    when you arrive on a project to have a file describing the context. The initial version of this script accepted definition of the prerequisites in the command line or environment variables but sometimes flexibility does not help.

    The only exception to the rule above is the password to avoid the hassle of not keeping the setenv file under source control or managing encrypted credentials.
"""

class MySQLNotRunningError(Exception):
    """Custom exception for when MySQL is not running."""
    pass

class ApacheNotRunningError(Exception):
    """Custom exception for when Apache is not running."""
    pass

# Custom formatter to preserve line breaks
class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    pass

def parse_environment() -> Dict[str, Any]:
    """
    Parse the command line arguments. Checks that mandatory parameters are set. returns a dictionary of CLI arguments.
    The following parameters can be set:
    - verbose: verbose mode
    - create_db: boolean to create the databases if they do not exist (default: False)
    - config: path to a configuration file
    """

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Check Prerequisites for local WEB applications",
                                     formatter_class=CustomHelpFormatter,
                                     epilog="""\
The configuration file is a python file that defines the prerequisites to check. It must define the following variables:
    databases: databases that must exist
    user: database connection user
    urls: URLs to check
    tables: tables that must exist
""")
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-p", "--password", help="Password for MySQL server (optional)")
    parser.add_argument("--create_db", action="store_true", default=False, help="Create databases if they do not exist")
    parser.add_argument("--create_table", action="store_true", default=False, help="Create tables if they do not exist")
    parser.add_argument("-c", "--config", help="Path to a configuration file", default="setenv.py", required=False)
    parser.add_argument("-u", "--user", help="Username for MySQL server (optional)")

    # Parse command line arguments
    args = parser.parse_args()

    # Create a dictionary to store the final configuration
    config: Dict[str, Any] = {}

    # Process each parameter
    config['verbose'] = args.verbose or os.environ.get('VERBOSE', '').lower() == 'true'
    config['create_db'] = args.create_db
    config['create_table'] = args.create_table
    config['config'] = args.config

    # Check if the configuration file exist
    if config['config'] and not os.path.exists(config['config']):
        print(f"Configuration file {config['config']} does not exist")
        exit(1)
    else:
        conf_file = config['config']
        print("Using configuration file:", conf_file)
        spec = importlib.util.spec_from_file_location("config", conf_file)
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)

    # make the parameters defined in the configuration file available in the config dictionary
    if hasattr(cfg, 'databases'): config['databases'] = cfg.databases
    if hasattr(cfg, 'user'): config['user'] = cfg.user
    if hasattr(cfg, 'password'): config['password'] = cfg.password
    if hasattr(cfg, 'urls'): config['urls'] = cfg.urls

    # CLI credentials have highest priority than configuration file

    if args.password: config['password'] = args.password
    if args.user: config['user'] = args.user


    # Check for mandatory parameters
    mandatory_params = ['user', 'password', 'databases']

    missing_params = False
    for param in mandatory_params:
        if param not in config:
            print(f"Missing mandatory parameter: {param}")
            missing_params = True

    if missing_params:
        print("Exiting.")
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
# Main
#######################################################################
print ("Prerequisites :")

config = parse_environment()

if config['verbose']: print ("Configuration:", config)

check_apache()
print ("Apache is running")

check_mysql(host='localhost', user=config['user'], password=config['password'])
print ("MySql is running")

results = check_urls(config['urls'])
print("URL:")
for url, status in results.items():
    print(f"\t{url} - Status: {status}")

php_version = check_php_version()
print(f"Current PHP version: {php_version}")

host = "localhost"
user = config['user']
password = config['password']

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