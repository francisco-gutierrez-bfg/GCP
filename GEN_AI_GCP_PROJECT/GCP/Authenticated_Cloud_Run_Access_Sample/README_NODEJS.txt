Created by: Francisco Gutierrez G.
            Unix/Linux Architect and Cloud Enginner 
            Globallogic 2025

Accessing a Cloud Run Service Authenticated from Node.js and JavaScript using a Service Account JSON Key
----------------------------------------------------------------------------------------------------------

This document describes how to authenticate and call a Cloud Run service using Node.js with a service account JSON key.

Requirements:
-------------
- Node.js 14+
- Install the required Node.js packages:
    npm install google-auth-library axios
- Service Account Key json file --> Inside folder [SA_cloud_run_access_apps]

Configuration:
--------------
You need:
- A service account JSON key file.
- Your Cloud Run HTTPS URL.

The service account must have the 'roles/run.invoker' permission on the Cloud Run service.

JavaScript Code Example:
-------------------------

1. **GET Request to Cloud Run:**

const { GoogleAuth } = require('google-auth-library');
const axios = require('axios');

const SERVICE_ACCOUNT_FILE = 'path/to/your-service-account.json';
const CLOUD_RUN_URL = 'https://your-cloud-run-url.run.app';
const AUDIENCE = CLOUD_RUN_URL;

async function callCloudRun() {
  const auth = new GoogleAuth({
    keyFile: SERVICE_ACCOUNT_FILE,
    scopes: 'https://www.googleapis.com/auth/cloud-platform',
  });

  const client = await auth.getIdTokenClient(AUDIENCE);

  const res = await client.request({ url: CLOUD_RUN_URL });

  console.log('Status code:', res.status);
  console.log('Response body:', res.data);
}

callCloudRun().catch(console.error);

2. **POST Request with JSON Payload to Cloud Run:**

const { GoogleAuth } = require('google-auth-library');
const axios = require('axios');

const SERVICE_ACCOUNT_FILE = 'path/to/your-service-account.json';
const CLOUD_RUN_URL = 'https://your-cloud-run-url.run.app';
const AUDIENCE = CLOUD_RUN_URL;

async function postToCloudRun() {
  const auth = new GoogleAuth({
    keyFile: SERVICE_ACCOUNT_FILE,
    scopes: 'https://www.googleapis.com/auth/cloud-platform',
  });

  const client = await auth.getIdTokenClient(AUDIENCE);

  const payload = {
    key1: 'value1',
    key2: 'value2',
  };

  const res = await client.request({
    url: CLOUD_RUN_URL,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: payload,
  });

  console.log('Status code:', res.status);
  console.log('Response body:', res.data);
}

postToCloudRun().catch(console.error);

Important Notes:
----------------
- Always use HTTPS for Cloud Run services.
- Ensure that the service account JSON file includes the 'private_key' section.
- The 'target_audience' must exactly match your Cloud Run URL.
- 'google-auth-library' automatically handles token refreshes.
