
#########################################################
# OLENBEE GCP PROJECT STRUCTURE AND DEPLOYMENT WORKFLOW #
#########################################################

+----------------------------------------+
| Author: Francisco JAvier Gutierrez.    |
| Senior Unix/Linux & Cloud Ops Engineer |
| Globallogic.                           |
+----------------------------------------+

=======================
|| Table of Contents ||
=======================
- [Introduction]
- [OlenBee GCP Projects Structure]
  - [Organization Level]
  - [STANDARD Folder (Parent Folder)]
    - [Infrastructure]
    - [Billing]
    - [Network]
    - [Security]
    - [DEV (Development Applications)]
- [OlenBee GCP Structure Tree]
- [GitHub Repositories]
- [GitHub Actions Deployment Process]
  - [Branching and Approval Process]
  - [Commit and Merge Strategy]
  - [Deployment Workflow]
- [Building and Deployment Instructions]
  - [Deploying an app image and Cloud Run instance from GCLOUD CLI (From a local computer to GCP)]
  - [Image build and Cloud run deploy commands for each application]


Introduction
============
This document provides an overview of the Google Cloud Platform (GCP) project structure for Olenbee.com. 
It outlines the hierarchical organization of resources, including infrastructure, networking, security, billing, and production applications. 
The structure is designed to ensure efficient resource management, security enforcement, cost control, and streamlined application deployment.

Additionally, this document describes the GitHub Actions deployment process, which automates application deployments to Google Container Registry (GCR) / Google Artifact Registry (GAR). 
It also details how GitHub is securely integrated with GCP using Workload Identity Federation to manage authentication and access control.

This structured approach ensures scalability, security, and operational efficiency while maintaining clear separation between different functional areas.


OlenBee GCP Projects Structure:
===============================
This hierarchical model enables efficient resource management, security enforcement, cost control, and scalability while ensuring a clear separation between different functional areas. 
Each folder and project is designed to serve a specific purpose, reducing complexity and improving operational efficiency across Olenbee.com’s GCP environment.

The organization follows a structured approach to managing resources, security, networking, billing, and application deployments through a well-defined folder and project hierarchy.

Organization Level
------------------
At the top level, the Olenbee.com organization acts as the root entity, encapsulating all projects and resources under a unified management structure.

 STANDARD Folder (Parent Folder)
 ...............................
 The STANDARD folder serves as the primary container for all infrastructure components, security configurations, and production applications. It ensures a logical separation of concerns and facilitates centralized governance and access control.

 Infrastructure
 ..............
 Contains essential services required for auditing and monitoring across all projects.
 Includes dedicated audit projects for different environments (e.g., olb-audit-hprd, olb-audit-prd).

 Billing
 .......
 Responsible for cost management and billing control across all GCP projects.
 Dedicated projects (olb-billing-prd) to track and optimize expenditures.

 Network
 .......
 Manages network configurations for application environments, including PRD, DEV, PPRD, QA, and UAT.
 Includes Hub-and-Spoke architecture, where olb-nethub-prd acts as the central hub and various olb-netspoke projects manage connectivity per environment.
 
 Note: All projects use a shared VPC comming from olb-nethub-<env>, being <env> each environment (prd,dev, uat, qa)
       The app projects need to be related inside VPC --> Shared VPC section in order to be visible and usable on the destination app project.

 Security
 ........
 Centralized security configurations for all application environments.
 Projects like olb-security-prd ensure compliance and enforcement of security policies.

 DEV (Development Applications)
 .............................
 Houses all development workloads, ensuring a clear distinction between infrastructure and application projects.

 Contains critical application components:
  - Beneficiaries-API (e.g., olb-beneficiaries-api-dev)
  - Clients-WEBAPP, with separated Backend (API services) and Frontend (User interfaces).
  - Olenbee-BO (Backoffice services), structured similarly to Clients-WEBAPP.


OlenBee GCP Structure Tree
==========================
The OlenBee GCP Structure Tree represents the hierarchical organization of Google Cloud Platform (GCP) resources within the Olenbee.com environment. 
Each section is designed to streamline operations, enhance security, and ensure cost efficiency while maintaining clear separation between different functional areas within the organization.

The structure is divided into key sections:
...........................................
 - Infrastructure – Manages audit and monitoring for all projects.
 - Billing – Controls and tracks cloud service costs.
 - Network – Defines networking configurations for different environments (PRD, DEV, PPRD, QA, UAT).  
   Note: All projects use a shared VPC comming from olb-nethub-<env>, being <env> each environment (prd,dev, uat, qa)
       The app projects need to be related inside VPC --> Shared VPC section in order to be visible and usable on the destination app project.

 - Security – Manages security policies and access controls.
 - Production (PRD) – Hosts production applications, including backend and frontend services.

  olenbee.com  <-- Organization
  |
  └── STANDARD <-- Parent Folder
      |    
      ├── Infrastructure  
      |   |
      │   └── Audit  --> Audit and monitoring for all projects
      |       |
      │       ├── olb-audit-hprd  
      │       ├── olb-audit-hprd-f288  
      │       ├── olb-audit-prd  
      │       └── olb-audit-prd-37cb
      |  
      ├── Billing  --> Billing control for all projects
      |   |
      │   ├── olb-billing-prd  
      │   └── olb-billing-prd-7cad  
      |
      ├── Network  ---> Network configurations for App Projects (PRD - DEV - PPRD - QA - UAT)
      |   |_ Note: All projects use a shared VPC comming from olb-nethub-<env>, being <env> each environment (prd,dev, uat, qa)
      |   |        The app projects need to be related inside VPC --> Shared VPC section in order to be visible and usable on the destination app project.
      |   |
      │   ├── olb-nethub-prd  (olb-nethub-prd-e7ce) 
      │   ├── olb-netspoke-dev (olb-netspoke-dev-6005) 
      │   ├── olb-netspoke-pprd (olb-netspoke-pprd-b534) 
      │   ├── olb-netspoke-prd (olb-netspoke-prd-39fa)  
      │   ├── olb-netspoke-qa (olb-netspoke-qa-4b74)
      │   └── olb-netspoke-uat (olb-netspoke-uat-8f33) 
      |
      ├── Security  ---> Security Configuirations for App Projects (PRD - DEV - PPRD - QA - UAT)
      |   |
      │   ├── olb-security-hprd (olb-security-hprd-9395) 
      │   └── olb-security-prd 
      | 
      └── DEV  ---> Development APPS
          |
          ├── Beneficiaries-API 
          |   | 
          │   └── olb-beneficiaries-api-dev  
          |
          ├── Clients-WEBAPP
          |   |  
          │   ├── Backend  
          │   │   └── olb-clientsapp-api-dev  
          │   └── Frontend  
          │       └── olb-clientsapp-front-dev
          | 
          └── Olenbee-BO  
              |
              ├── Backend  
              │   └── olb-backoffice-api-dev
              └── Frontend  
                  └── olb-backoffice-front-dev 


GitHub Repositories:
====================

 - MS-APPDATA:
   API for Beneficiaries App
   Link: https://github.com/olenbee/ms-appdata

 - MSS-APPCLIENT-API:
   API for Clients website
   Link: https://github.com/olenbee/ms-appclient-api

 - MS-APPCLIENT:
   Front End for Clients Web
   Link: https://github.com/olenbee/ms-appclient

 - BACKOFFICESERVICE:
   API for the Backoffice Web site
   Link: https://github.com/olenbee/backofficeservice

 - BACKOFFICECLIENT:
   Front End for Backoffice webapp
   Link: https://github.com/olenbee/backofficeclient


GitHub Actions Deployment Process
---------------------------------
Each project in olenbee.com has a dedicated GitHub Actions pipeline responsible for deploying application images to Google Container Registry (GCR) / Google Artifact Registry (GAR) within GCP.

Branching and Approval Process
------------------------------
Every GitHub repository has 5 branches

 Development → Used for active development and testing. This is where new features, bug fixes, and changes are initially committed. Developers typically work on feature branches that are later merged into the development branch.

 QA (Quality Assurance) → Used for testing after development. Code from the development branch is merged into the QA branch to verify functionality, performance, and stability before progressing to the next stage.

 UAT (User Acceptance Testing) → Used for final testing by end-users or business stakeholders. This branch ensures that the software meets business requirements and works as intended in a controlled environment.

 Preproduction → A staging environment that closely mirrors production. Code in this branch is tested to simulate real-world usage before deployment to production.

 Production → The final branch used for live releases. It is restricted to ensure stability and controlled releases, meaning only thoroughly tested and approved code is merged into this branch.

Commit and merge strategy:
--------------------------
Merging into Production requires two approver's consent before the deployment workflow can be executed.

Deployment Workflow
-------------------
1- The GitHub Action is triggered after an approved commit is merged into the repository.
2- The pipeline builds the application image and pushes it to GCR/GAR.
3- The deployment process is automated and follows a secure authentication mechanism by using "GCP Workload Identity Federation"
   to securely connect GitHub Actions to GCP without requiring service account keys.
   The GitHub workflow assumes a GCP service account named olenbee-deployment-pipeline, which has permissions to push images and deploy applications.
   This setup enhances security by eliminating the need for static credentials while ensuring granular access control.


Building and Deployment Instructions
====================================
There ware two ways to deploy apps:
 - By using GitHub Actions workflows (Described previously)
 - By using GCLOUD SDK CLI from your computer (manually, described below)

The following instructions provide a comprehensive guide to deploying application images and Cloud Run instances on Google Cloud Platform (GCP) using the GCLOUD CLI from a local computer. 
It outlines the prerequisites, necessary configurations, and step-by-step procedures to ensure a successful deployment.

Ths section covers:
...................
 - Installing and configuring GCLOUD SDK
 - Building and pushing Docker images to Google Artifact Registry (GAR)
 - Deploying applications on Cloud Run with appropriate settings, including service accounts and VPC configurations

Additionally, specific deployment instructions are provided for multiple applications, ensuring clarity and consistency. 
This document serves as a practical reference for engineers working with GCP infrastructure.


Deploying an app image and Cloud Run instance from GCLOUD CLI (From a local computer to GCP)
--------------------------------------------------------------------------------------------
This guide outlines the process for deploying an application image and a Cloud Run instance using the GCLOUD CLI from a local computer to Google Cloud Platform (GCP). 
It covers prerequisites, setup, image building, and deployment procedures.

Prereqs:
........
Before starting, ensure the following prerequisites are met:
 - GCLOUD SDK installed
 - GCP project filly setup to be used.

Procedure:
..........
Follow these steps to deploy your application:

1- Install GCLOUD SDK on your computer

2- Login your CLI 
   - gcloud init
   - gcloud auth config
     - Use your GCP account
     - The system will open a browser, please follow the instructions

3- Build an image from a Dockerfile
   - Go to the same directory where the Docker file resides.
   - Buld the image:
     docker build -t europe-west9-docker.pkg.dev/<gcp project name>/<gcp-GAR-repo-name>/<image-name> .  <-- The image name should be called the same as the destination GAR repo at GCP
   - Push the in¿mage to the right GCP GAR repository:
     docker psuh europe-west9-docker.pkg.dev/<gcp project name>/<gcp-GAR-repo-name>/<image-name> <-- This will upload the image into the right GCP GAR Repo
     Note: Please check if the image was deployed with an SHA hash attached to the name, if so, please add the hash the image name in the deployed command.
           This can be added if the GitHub action file has that specific instruction during the image build and push steps.
           Ex:
              europe-west9-docker.pkg.dev/<gcp project name>/<gcp-GAR-repo-name>/<image-name>@sha256:0e88c194d2bf686afa2528a073cbe83c5571ed2676d6e0c8ece8258cafe3a872 
              So, the push should be as follows:
              - docker push europe-west9-docker.pkg.dev/<gcp project name>/<gcp-GAR-repo-name>/<image-name>@sha256:0e88c194d2bf686afa2528a073cbe83c5571ed2676d6e0c8ece8258cafe3a872 

4- Deploy the Cloud Run instance

   gcloud run deploy <app or instance name> \
       --image europe-west9-docker.pkg.dev/<gcp project name>/<gcp-GAR-repo-name>/<image-name>:latest \
       --region europe-west9 \
       --platform managed \
       --service-account clourun-olenbee@<gcp project name>.iam.gserviceaccount.com \
       --memory <RAM>Gi \
       --cpu <Num of CPU's> \
       --vpc-connector projects/<gcp project name>/locations/europe-west9/connectors/olb-prd-network-glb-netspoke \
       --vpc-egress all-traffic \
       --port 8080
       --allow-unauthenticated


Image build and Cloud run deploy commands for each application:
---------------------------------------------------------------

ClientsApp API Dev:
...................
This section provides instructions for building and deploying the ClientsApp API in a dev environment.

1- Build your image from the Dockerfile
   - docker build -t europe-west9-docker.pkg.dev/olb-clientsapp-api-dev/clientsapp/clientsapp .
   - docker psuh europe-west9-docker.pkg.dev/olb-clientsapp-api-dev/clientsapp/clientsapp:latest

2- Deploy the Cloud Run instance

gcloud run deploy clienstapp \
    --image europe-west9-docker.pkg.dev/olb-clientsapp-api-dev/clientsapp/clientsapp:latest \
    --region europe-west9 \
    --platform managed \
    --service-account clourun-olenbee@olb-clientsapp-api-dev.iam.gserviceaccount.com \
    --vpc-connector projects/olb-clientsapp-api-dev/locations/europe-west9/connectors/olb-dev-network-glb-netspoke \
    --vpc-egress all-traffic \
    --port 8080 \
    --allow-unauthenticated
   


ClientsApp Front Dev:
.....................
This section outlines the steps to build and deploy the frontend application for ClientsApp in a dev environment.

1- Build your image from the Dockerfile
   - docker build -t europe-west9-docker.pkg.dev/olb-clientsapp-front-dev/clientsapp-front/clientsapp-front .
   - docker psuh europe-west9-docker.pkg.dev/olb-clientsapp-front-dev/clientsapp-front/clientsapp-front:latest

2- Deploy the Cloud Run instance

gcloud run deploy clientsapp-front \
   --image europe-west9-docker.pkg.dev/olb-clientsapp-front-dev/clientsapp-front/clientsapp-front:latest \
   --region europe-west9 \
   --platform managed \
   --service-account clourun-olenbee@olb-clientsapp-front-dev.iam.gserviceaccount.com \
   --vpc-connector projects/olb-clientsapp-api-dev/locations/europe-west9/connectors/olb-dev-network-glb-netspoke \
   --vpc-egress all-traffic \
   --port 8080 \
   --allow-unauthenticated


Backoffice API Dev:
...................
This section details the process for deploying the Backoffice API in production.

1- Build your image from the Dockerfile
   - docker build -t europe-west9-docker.pkg.dev/olb-backoffice-api-dev/backoffice/backoffice .
   - docker psuh europe-west9-docker.pkg.dev/olb-backoffice-api-dev/backoffice/backoffice:latest

2- Deploy the Cloud Run instance

gcloud run deploy backoffice \
    --image europe-west9-docker.pkg.dev/olb-backoffice-api-dev/backoffice/backoffice:latest \
    --region europe-west9 \
    --platform managed \
    --service-account clourun-olenbee@olb-backoffice-api-dev.iam.gserviceaccount.com \
    --vpc-connector projects/olb-backoffice-api-dev/locations/europe-west9/connectors/olb-dev-network-glb-netspoke \
    --vpc-egress all-traffic \
    --port 8080 \
    --allow-unauthenticated


Backoffice Front Dev:
.....................
This section provides steps for deploying the frontend interface of the Backoffice application in dev.


1- Build your image from the Dockerfile
   - docker build -t europe-west9-docker.pkg.dev/olb-backoffice-front-dev/backofficefront/backofficefront .
   - docker psuh europe-west9-docker.pkg.dev/olb-backoffice-front-dev/backofficefront/backofficefront:latest

2- Deploy the Cloud Run instance

gcloud run deploy backofficefront \
   --image europe-west9-docker.pkg.dev/olb-backoffice-front-dev/backofficefront/backofficefront@sha256:4f1dd64c14b1e780a581e5704c697bf4d18a09ebfcb39929346b3219b22881d6 \
   --region europe-west9 \
   --platform managed \
   --service-account clourun-olenbee@olb-backoffice-front-dev.iam.gserviceaccount.com \
   --vpc-connector projects/olb-backoffice-api-dev/locations/europe-west9/connectors/olb-dev-network-glb-netspoke \
   --vpc-egress all-traffic \
   --port 8080 \
   --allow-unauthenticated


Beneficiaries API Dev:
.......................
This section describes the process for deploying the Beneficiaries API in a dev environment.

1- Build your image from the Dockerfile
   - docker build -t europe-west9-docker.pkg.dev/olb-beneficiaries-api-dev/ms-appdata/ms-appdata .
   - docker psuh europe-west9-docker.pkg.dev/olb-beneficiaries-api-dev/ms-appdata/ms-appdata:latest

2- Deploy the Cloud Run instance

gcloud run deploy ms-appdata \
   --image europe-west9-docker.pkg.dev/olb-beneficiaries-api-dev/ms-appdata/ms-appdata@sha256:0e88c194d2bf686afa2528a073cbe83c5571ed2676d6e0c8ece8258cafe3a872 \
   --region europe-west9 \
   --platform managed \
   --service-account clourun-olenbee@olb-beneficiaries-api-dev.iam.gserviceaccount.com \
   --vpc-connector projects/olb-clientsapp-api-dev/locations/europe-west9/connectors/olb-dev-network-glb-netspoke \
   --vpc-egress all-traffic \
   --port 8080 \
   --allow-unauthenticated

By following above steps, users can effectively deploy applications using the GCLOUD CLI, ensuring a smooth and automated process for managing Cloud Run instances.



