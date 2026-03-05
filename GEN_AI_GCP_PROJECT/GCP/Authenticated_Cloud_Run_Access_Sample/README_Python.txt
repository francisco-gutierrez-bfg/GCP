Created by: Francisco Gutierrez G.
            Unix/Linux Architect and Cloud Enginner 
            Globallogic 2025

Accessing a Cloud Run Service Authenticated from Python using a Service Account JSON Key
------------------------------------------------------------------------------------------

This document describes how to authenticate and call a Cloud Run service using Python with a service account JSON key.

Requirements:
-------------
- Python 3.7+
- Install the required Python packages:
    pip install google-auth requests
- Service Account Key json file --> Inside folder [SA_cloud_run_access_apps]

Configuration:
--------------
You need:
- A service account JSON key file.
- Your Cloud Run HTTPS URL.

The service account must have the 'roles/run.invoker' permission on the Cloud Run service.

Python Code Example:
---------------------

1. **GET Request to Cloud Run:**

import json
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

SERVICE_ACCOUNT_FILE = "path/to/your-service-account.json"
CLOUD_RUN_URL = "https://your-cloud-run-url.run.app"
AUDIENCE = CLOUD_RUN_URL

credentials = service_account.IDTokenCredentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    target_audience=AUDIENCE
)

request = google.auth.transport.requests.Request()
credentials.refresh(request)

id_token = credentials.token

headers = {
    "Authorization": f"Bearer {id_token}",
}

response = requests.get(CLOUD_RUN_URL, headers=headers)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text}")

2. **POST Request with JSON Payload to Cloud Run:**

import json
import google.auth.transport.requests
from google.oauth2 import service_account
import requests

SERVICE_ACCOUNT_FILE = "path/to/your-service-account.json"
CLOUD_RUN_URL = "https://your-cloud-run-url.run.app"
AUDIENCE = CLOUD_RUN_URL

credentials = service_account.IDTokenCredentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    target_audience=AUDIENCE
)

request = google.auth.transport.requests.Request()
credentials.refresh(request)

id_token = credentials.token

headers = {
    "Authorization": f"Bearer {id_token}",
    "Content-Type": "application/json"
}

payload = {
    "key1": "value1",
    "key2": "value2"
}

response = requests.post(CLOUD_RUN_URL, headers=headers, json=payload)

print(f"Status code: {response.status_code}")
print(f"Response body: {response.text}")

Important Notes:
----------------
- Always use HTTPS for Cloud Run services.
- Ensure that the service account JSON file includes the 'private_key' section.
- The 'target_audience' must exactly match your Cloud Run URL.
- The 'Content-Type: application/json' header must be included when sending JSON payloads.
