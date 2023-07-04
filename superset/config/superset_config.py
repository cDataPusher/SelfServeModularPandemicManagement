import os

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset@db:5432/superset"

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []

# Whether to run the web server in debug mode or not
DEBUG = True

# Whether to show the stacktrace in 500 error pages
SHOW_STACKTRACE = True

# Enable this to store the log in a .log file.
ENABLE_FILE_LOG = False

# Superset web server workers number
SUPERSET_WEBSERVER_WORKERS = 2

# Superset web server port
SUPERSET_WEBSERVER_PORT = 8088

TESTING = 1

# Enable / disable scheduled email reports
ENABLE_SCHEDULED_EMAIL_REPORTS = False

# Whether to run the web server in threaded mode
THREADED = True

# Keycloak switch
ENABLE_KEYCLOAK = os.getenv("ENABLE_KEYCLOAK", "false").lower() == "true"

# Superset secret key
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")
SUPERSET_SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

if ENABLE_KEYCLOAK:
    # Keycloak configuration
    AUTH_TYPE = AUTH_OAUTH
    AUTH_ROLE_ADMIN = "Admin"
    AUTH_ROLE_PUBLIC = "Public"
    AUTH_USER_REGISTRATION = True
    AUTH_USER_REGISTRATION_ROLE = "Public"
    OAUTH_PROVIDERS = [
        {
            "name": "keycloak",
            "token_key": "access_token",
            "icon": "fa-key",
            "remote_app": {
                "api_base_url": os.getenv("KEYCLOAK_BASE_URL"),
                "client_kwargs": {
                    "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
                    "client_secret": os.getenv("KEYCLOAK_CLIENT_SECRET"),
                },
            },
        }
    ]
