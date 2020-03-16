# INSTRUCTIONS:  #
##################
# please refer to the README and the project wiki for the most up-to-update information.
# If you want to customize this app, duplicate this file and rename it to my_conf.py and make changes
# through that file. The 'my_conf.py' file is in the .gitignore
# As this file in a part of the repository, please do not make any customizations here

import os
from decouple import config
from .utils import db_connection_values_exist, get_db_connection_dict

########
# APPS #
########

# add new applications to this dictionary; grey out any app you do not want
# the dict key should be the actual name of the app
# if there is a verbose name, it should be the key value, otherwise None
APP_DICT = {
    'inventory': 'Metadata Inventory',
    'grais': 'grAIS',
    'oceanography': 'Oceanography',
    'herring': 'HerMorrhage',
    'camp': 'CAMP db',
    'meq': 'Marine environmental quality (MEQ)',
    'diets': 'Marine diets',
    'projects': 'Science project planning',
    'ihub': 'iHub',  # dependency on masterlist
    'scifi': 'SciFi',
    'masterlist': 'Masterlist',
    'shares': 'Gulf Shares',
    'travel': 'Travel Management System',
    'sar_search': "SAR Search",
    'spot': 'Grants & Contributions (Spot)',  # dependency on masterlist, sar_search
    'ios2': 'Instruments',
    'staff': "Staff Planning Tool",
    'publications': "Project Publications Inventory",
    'trapnet': "TrapNet",
    'whalesdb': "Whale Equipment Deployment Inventory",
    'vault': "Marine Megafauna Media Vault",
}

# This variable is used to employ a preconfiguartion of applications for Azure deployment
DEPLOYMENT_STAGE = config("DEPLOYMENT_STAGE", cast=str, default="").upper()

### Deploying application in production - don't change, unless you know what you're doing
if DEPLOYMENT_STAGE == 'PROD':
    # overwrite app_dict with only the applications to be deployed to PROD
    APP_DICT = {
        'travel': 'Travel Management System'
    }

### Deploying application in test environment
elif DEPLOYMENT_STAGE == 'TEST':
    # overwrite app_dict with only the applications to be deployed to TEST
    APP_DICT = {
        'travel': 'Travel Management System'
    }


elif DEPLOYMENT_STAGE == 'DEV':
    # no changes to make, just a placeholder
    pass

MY_INSTALLED_APPS = [app for app in APP_DICT]

#############
# DATABASES #
#############

# By default, the application will use the setting from the environment variables (or .env file).
# If those variables are not set, the local db will be created. If you would like to use a local db
# disrespective of the environment variables, set it to True
USE_LOCAL_DB = False

# get the connection information from the env; if not all values present, default to local db
db_connections = get_db_connection_dict()
if not db_connection_values_exist(db_connections):
    USE_LOCAL_DB = True
    print("DB connection values are not specified. Can not connect to the database. Connecting to local db instead.")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if USE_LOCAL_DB:
    my_default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    DB_MODE = "LOCAL"
    DB_NAME = "db.sqlite3"
    DB_HOST = "local"
else:

    my_default_db = {
        'ENGINE': 'django.db.backends.mysql',
        'TIME_ZONE': 'America/Halifax',
        'OPTIONS': {
            'host': db_connections["DB_HOST"],
            'port': db_connections["DB_PORT"],
            'database': db_connections["DB_NAME"],
            'user': db_connections["DB_USER"],
            'password': db_connections["DB_PASSWORD"],
            'init_command': 'SET default_storage_engine=INNODB',
        }}

    # if we have a connection, get the names of db and host to pass in as context processors
    DB_NAME = db_connections["DB_NAME"]
    DB_HOST = db_connections["DB_HOST"]

    # give the user an option to not define the db mode. If not provided, it will be guessed at from the host name
    if not db_connections["DB_MODE"]:
        # Determine which DB we are using from the host name"
        if "dmapps-dev-db" in db_connections["DB_HOST"] and db_connections["DB_NAME"] == "dmapps":
            DB_MODE = "DEV"
        elif  "dmapps-dev-db" in db_connections["DB_HOST"] and db_connections["DB_NAME"] == "dmapps-test":
            DB_MODE = "TEST"
        elif  "dmapps-prod-db" in db_connections["DB_HOST"]:
            DB_MODE = "PROD"
    else:
        DB_MODE = db_connections["DB_MODE"]

DATABASES = {
    'default': my_default_db,
}