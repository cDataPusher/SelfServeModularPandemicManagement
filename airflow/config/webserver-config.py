#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Default configuration for the Airflow webserver."""
from __future__ import annotations
import logging
import os
from distutils.util import strtobool

from airflow.www.security import AirflowSecurityManager
from airflow.www.fab_security.manager import AUTH_DB, AUTH_OAUTH

log = logging.getLogger(__name__)
# from airflow.www.fab_security.manager import AUTH_LDAP
# from airflow.www.fab_security.manager import AUTH_OAUTH
# from airflow.www.fab_security.manager import AUTH_OID
# from airflow.www.fab_security.manager import AUTH_REMOTE_USER

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# For details on how to set up each of the following authentication, see
# http://flask-appbuilder.readthedocs.io/en/latest/security.html# authentication-methods
# for details.

class MySecurityManager(AirflowSecurityManager):
    def get_oauth_user_info(self, provider, resp):
        if provider == "keycloak":
            id_token = resp["id_token"]
            me = self._azure_jwt_token_parse(id_token)
            try:  # this fails/blocks login if no roles assigned
                role_keys = me["resource_access"][os.getenv("KEYCLOAK_CLIENT_ID")]["roles"]
            except:
                role_keys = []
            return {
                "username": me.get("preferred_username", ""),
                "first_name": me.get("given_name", ""),
                "last_name": me.get("family_name", ""),
                "email": me.get("email", ""),
                "role_keys": role_keys,
            }
        else:
            return {}

SECURITY_MANAGER_CLASS = MySecurityManager

# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_OAUTH : Is for OAuth
# AUTH_TYPE = AUTH_DB

if os.getenv("KEYCLOAK_AUTH") and os.getenv("KEYCLOAK_AUTH").lower() == "true":
    logging.info("Using AUTH_OAUTH")
    AUTH_TYPE = AUTH_OAUTH
    # force users to re-auth after 1h of inactivity (to keep roles in sync)
    PERMANENT_SESSION_LIFETIME = 3600

    # if we should replace ALL the user's roles each login, or only on registration
    AUTH_ROLES_SYNC_AT_LOGIN = strtobool(
        os.getenv("KEYCLOAK_ROLES_SYNC_AT_LOGIN", "false")
    )
    logging.info(f"Synchronizing auth roles at login: {AUTH_ROLES_SYNC_AT_LOGIN}")
    if AUTH_ROLES_SYNC_AT_LOGIN:
        # Default airflow roles, do not remove
        AUTH_ROLES_MAPPING = {
            "User": ["DataProcessors"],
            "Admin": ["Admin"],
            "Viewer": ["DataUsers"],
            "Op": ["DataSuppliers"],
            "Public": ["Public"],
        }

        # read additional roles from 'KEYCLOAK_CUSTOM_ROLES' Env for syncing
        if os.getenv("KEYCLOAK_CUSTOM_ROLES") and os.getenv("KEYCLOAK_CUSTOM_ROLES") != "":
          ROLES = os.getenv("KEYCLOAK_CUSTOM_ROLES")
          AUTH_ROLES_MAPPING.update({key: [key] for key in ROLES.split(" ")})
          logging.info(f"updated roles: {AUTH_ROLES_MAPPING}")
        else:
          logging.info(f"no additional roles added.")
        
    # When using OAuth Auth, uncomment to setup provider(s) info
    OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "token_key": "access_token",
        "icon": "fa-user-circle",
        "remote_app": {
            "server_metadata_url": os.getenv("KEYCLOAK_BASE_URL") + "/realms/" + os.getenv("KEYCLOAK_REALM") + "/.well-known/openid-configuration",
            "authorize_url": os.getenv("KEYCLOAK_BASE_URL") + "/realms/" + os.getenv("KEYCLOAK_REALM") + "/protocol/openid-connect/auth",
            "access_token_url": os.getenv("KEYCLOAK_BASE_URL") + "/realms/" + os.getenv("KEYCLOAK_REALM") + "/protocol/openid-connect/token",
            "client_kwargs": {"scope": "openid profile email roles"},
            "client_id": os.getenv("KEYCLOAK_CLIENT_ID"),
            "client_secret": os.getenv("KEYCLOAK_CLIENT_SECRET"),
            },
        }
    ]

    LOGOUT_REDIRECT_URL = (
        os.getenv("KEYCLOAK_BASE_URL")
        + "/realms/" 
        + os.getenv("KEYCLOAK_REALM")
        + "/protocol/openid-connect/logout?post_logout_redirect_uri="
        + os.getenv("AIRFLOW__WEBSERVER__BASE_URL")
        + "&client_id=" + os.getenv("KEYCLOAK_CLIENT_ID")
    )

else:
    logging.info("Using AUTH_DB")
    AUTH_TYPE = AUTH_DB

# Uncomment to setup Full admin role name
AUTH_ROLE_ADMIN = "Admin"

# Uncomment and set to desired role to enable access without authentication
# AUTH_ROLE_PUBLIC = "Viewer"

# Will allow user self registration
# AUTH_USER_REGISTRATION = True

# The recaptcha it's automatically enabled for user self registration is active and the keys are necessary
# RECAPTCHA_PRIVATE_KEY = PRIVATE_KEY
# RECAPTCHA_PUBLIC_KEY = PUBLIC_KEY

# Config for Flask-Mail necessary for user self registration
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'yourappemail@gmail.com'
# MAIL_PASSWORD = 'passwordformail'
# MAIL_DEFAULT_SENDER = 'sender@gmail.com'

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"

# Google OAuth example:
# OAUTH_PROVIDERS = [{
#   'name':'google',
#     'token_key':'access_token',
#     'icon':'fa-google',
#         'remote_app': {
#             'api_base_url':'https://www.googleapis.com/oauth2/v2/',
#             'client_kwargs':{
#                 'scope': 'email profile'
#             },
#             'access_token_url':'https://accounts.google.com/o/oauth2/token',
#             'authorize_url':'https://accounts.google.com/o/oauth2/auth',
#             'request_token_url': None,
#             'client_id': GOOGLE_KEY,
#             'client_secret': GOOGLE_SECRET_KEY,
#         }
# }]

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# When using OpenID Auth, uncomment to setup OpenID providers.
# example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
