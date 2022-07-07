"""
pip install --upgrade google-auth
pip install requests
"""

import google.auth  # for default authentication
import google.auth.transport.requests
from google.oauth2 import service_account  # for service account authentication
import logging


class GCP_Auth(object):

    def __init__(self, project_id: str=None, cred_path: str=None, scope: list=None, **kwargs):
        if scope is None:
            self.scope = []
            self.scope.append('https://www.googleapis.com/auth/cloud-platform')
        else:
            self.scope = scope

        try:
            if project_id is None or cred_path is None:
                self.credentials, self.project_id = google.auth.default(scopes=self.scope)
            else:
                self.credentials = service_account.Credentials.from_service_account_file(
                    cred_path).with_scopes(self.scope)
                self.project_id = project_id

        except Exception as e:
            logging.error(f"error: {e}")

        auth_req = google.auth.transport.requests.Request()
        self.credentials.refresh(auth_req)


    def _get_credentials(self):
        return self.credentials


    def _get_credentials_token(self):
        return self.credentials.token

