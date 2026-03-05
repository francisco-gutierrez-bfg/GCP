+----------------------------------------+
| Author: Francisco JAvier Gutierrez.    |
| Senior Unix/Linux & Cloud Ops Engineer |
| Globallogic.                           |
+----------------------------------------+

FIRST STEPS:
############

 - Setting up GitHub repositories
 - Setting up a new project in your cloud environment requires essential network configurations to ensure seamless connectivity and integration. 
 - Before starting development, it is mandatory to link the new project to the main network project and configure the necessary VPC settings.

This guide outlines the initial steps to:

 - Add the new project to the main network project, allowing it to inherit VPC settings.
 - Create a VPC Serverless Connector to enable serverless services to communicate with resources within the VPC.
 - Implement GitHub repositories for each project and environment.

By following these steps, your new project will be properly integrated into the network, ensuring efficient connectivity and security.


----------
Procedure:
----------

GCP:
++++
Create a new project in the respective folder.

Adding the new project to the network main project in order to give VPC settings to it:
=======================================================================================
- Once you create a new project:
  - Go to Infra --> Network --> olb-netspoke-<env> <-- (evv can be: dev,uat,qa,pprd,prod)
    - Go to VPC configurations --> Shared VPC --> Related projects
      - Add the new project.  


Create a VPC Serverless Connector in the network main project for the specific environment:
===========================================================================================
Please check the image file called "Prerquisite_Add_Connectors_to_each_network_project.png" in the main folder.

- Navigate to the VPC Connectors Section:

  - Go to VPC Network → Serverless VPC Access.
  - Click Create Connector.
  - Enter Connector Name:

    - In the Name field, enter the connector name in the format:
      olb-<project environment: prd, pprd, dev, qa, ust>-network-glb-netspoke

    - Select Region:
      Choose the appropriate region from the dropdown list.
      Example: europe-west9.
      Choose Network Type:

    - Select Shared VPC if using a host project.
      - Ensure the correct host project is displayed.
      - Select the Shared Network:
        The shared network should appear automatically. If not, check the host project settings.
      - Select the Subnet:
        Choose an available subnet from the dropdown.
        Ensure the subnet follows the required /28 IP range.
      - Finalize and Create:
        Click Create to deploy the connector.

Now your new project has access to network, subnetwork configurations and features.

Grant VPC ACCESS to service agent account:
==========================================
Go to the netspoke required project and run the following commands to add vpcaccess role to the service agent robot account:

Get the project number:
gcloud projects describe <project you just created> --format="value(projectNumber)"

Example:
========
gcloud projects describe olb-rolesservice-api-dev --format="value(projectNumber)"

Add the role:
=============
gcloud projects add-iam-policy-binding olb-netspoke-dev-6005 --member="serviceAccount:service-<Project Number>@serverless-robot-prod.iam.gserviceaccount.com" --role="roles/vpcaccess.user"

Example
=======
gcloud projects add-iam-policy-binding olb-netspoke-dev-6005 --member="serviceAccount:service-1094548230567@serverless-robot-prod.iam.gserviceaccount.com" --role="roles/vpcaccess.user"



GitHub:
+++++++

 - Sign In to GitHub
   Open a browser and go to: https://github.com
   Sign in with your GitHub account. If you don't have one, click "Sign Up" and create an account.
   Create a New Repository

 - After logging in, click the "+" icon at the top right corner of the page.
   Select "New repository" from the dropdown menu.
   Configure the Repository

     Repository name – Enter a unique name for the repository.
     Description – (Optional) Provide a short description of the repository.
     Visibility – Choose one of the following:
       Public – Anyone can see the repository.
       Private – Only you and invited collaborators can see it.
       (Optional) Check the following options:
         Add a README file – Adds a README.md file with an overview of the repository.
         Add .gitignore – Select a .gitignore template to exclude common files from being tracked (e.g., for Node.js, Python, etc.).
         Choose a license – Select a license for the repository (e.g., MIT, Apache 2.0).
     Click "Create repository."

 - Initialize the Repository (Optional)
   If you did not initialize the repository with a README file, you can do it manually:

 - Open a terminal or command prompt.
   Clone the repository:
   git clone https://github.com/your-username/your-repository.git

 - Navigate to the repository folder:
   cd your-repository
    Create a README.md file:
    echo "# Your Repository" >> README.md

 - Add the file to Git:
   git add README.md

 - Commit the file:
   git commit -m "Initial commit"

 - Push the changes to GitHub:
   git push origin main

 - Add files to the repository:
   git add .

 - Commit changes with a message:
   git commit -m "Add project files"
   
 - Push the changes:
   git push origin main

Repository Created and Updated

You can now manage the repository from the GitHub web interface or the command line.
