from google.oauth2 import service_account
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests
import webbrowser
import os

# Set the path to your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sa.json"

# Load service account credentials
source_credentials = service_account.Credentials.from_service_account_file(
    "sa.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

# Impersonate target service account
impersonated_creds = impersonated_credentials.Credentials(
    source_credentials=source_credentials,
    target_principal="clourun-glia@backoffice-optimization-dev.iam.gserviceaccount.com",
    target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
    lifetime=3600
)

# Prepare request object
auth_request = Request()

# 🎯 Generate ID token for Cloud Run
target_audience = "https://test-francisco-943792741697.us-central1.run.app"
id_token_value = id_token.fetch_id_token(auth_request, target_audience)

# Call the Cloud Run service
headers = {
    "Authorization": f"Bearer {id_token_value}"
}

response = requests.get(target_audience, headers=headers)

print("Status code:", response.status_code)
print("Response body:\n", response.text)

# Open the Cloud Run URL in the browser
if response.status_code == 200:
    print("Opening the Cloud Run service in your browser...")
    webbrowser.open(target_audience)
else:
    print("Failed to access Cloud Run, not opening browser.")
