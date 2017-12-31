import os
import sys

# Below Environment should exist in os.
# If below listed env variables are not found, then an error is raised.
# No need of assert statement. Just make sure variable is in list below
ENVIRON_VARIABLES = [
    'ENVIRON',
    'PRODUCTION',
    'DEV',
    'DEBUG',
    'DB_NAME',
    'MYSQL_USER',
    'MYSQL_PASSWORD',
    'MYSQL_HOST',
    'MYSQL_PORT',
    'APP_URL',
    'APP_CLIENT_ID',
    'APP_CLIENT_SECRET',
]

self = sys.modules[__name__]
for env in ENVIRON_VARIABLES:
    value = os.environ[env]

    if value.isdigit():
        value = int(value)
    setattr(self, env, value)
