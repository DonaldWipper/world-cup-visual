import os
import sys
from urllib.parse import urlparse

# Register database schemes in URLs.
#urlparse.uses_netloc.append('mysql')


DATABASE_URL='mysql://b1df3776b2b56c:8b4b450a@us-cdbr-iron-east-04.cleardb.net/heroku_0c1d0ea4e380413?reconnect=true'


url = urlparse(DATABASE_URL)


try:

    # Check to make sure DATABASES is set in settings.py file.
    # If not default to {}

    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })


except Exception:
    print ('Unexpected error:', sys.exc_info())

print(url.path[1:])

