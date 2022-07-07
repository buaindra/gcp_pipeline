### Sample
```python
from gcp_auth import GCP_Auth

gcp_auth = GCP_Auth()

gcp_auth_credential = gcp_auth._get_credentials()
gcp_auth_credential_token = gcp_auth._get_credentials_token()
```