Introducción:
=============

En esta guía, se presentará un ejemplo práctico de un Dockerfile diseñado para crear un contenedor de Tomcat que se conecta a una base de datos de Cloud SQL. 
Además, se abordará la creación y configuración de una instancia de Cloud SQL, así como los pasos necesarios para desplegar dicha instancia en Cloud Run.


1. Crear un Dockerfile

---
# Utilizar la imagen base de Tomcat
FROM openjdk:17-jdk-alpine

# Download Cloud SQL Proxy
ADD https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 /cloud_sql_proxy

# Make the Cloud SQL Proxy executable
RUN chmod +x /cloud_sql_proxy

# Copy the JAR file into the container
COPY settings/appdata-stg.jar /appdata-stg.jar

# Create a directory for Cloud SQL sockets
RUN mkdir -p /cloudsql

EXPOSE 8080
---

# Define the entry point to run the Cloud SQL Proxy and the Spring application
ENTRYPOINT ["/bin/sh", "-c", "/cloud_sql_proxy -dir=/cloudsql -instances=central-apex-438817-p5:europe-west9:olenbeeappdata-stg=tcp:5432 & java -jar /appdata-stg.jar --spring.profiles.active=stg"]

2. Desplegar imagen en el artifact registry de GCP (GCR)

3. Crear la BD en Cloud SQL

Autenticarse en GCP:

gcloud auth login
gcloud config set project <PROJECT_ID>

# Crear instancia de Cloud SQL:

gcloud sql instances create <nombre de instancia> \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=<region deseada> \
  --enable-private-ip \
  --vpc=<nombre del vpc creado previamente> \
  --no-assign-public-ip

Ejemplo:

gcloud sql instances create appdata-stg \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=europe-west9 \
  --enable-private-ip \
  --vpc=vpn-net-olenbee \
  --no-assign-public-ip

# Crear una base de datos
gcloud sql databases create <nombre de la BD> --instance=<nombre de instancia donde residirá la Bd>

# Crear un usuario
gcloud sql users create postgres --instance=<nombre de instancia donde residirá la Bd> --password=<clave de usuario>

4. Instrucciones para Despliegue en Cloud Run

Autenticarse en GCP:

gcloud auth login
gcloud config set project <PROJECT_ID>

Construir la imagen de Docker:


docker build -t gcr.io/<PROJECT_ID>/mi-aplicacion .

Subir la imagen al Container Registry:

docker push gcr.io/<PROJECT_ID>/mi-aplicacion

Desplegar en Cloud Run:

gcloud run deploy <nombre de servicioo app> \
  --image gcr.io/<PROJECT_ID>/<imagen desplegada en el repo GCR>:<version/tag> \
  --platform managed \
  --vpc-connector projects/<PROJECT_ID>/locations/<region>/connectors/<vpc> \
  --allow-unauthenticated \
  --service-account <service account asignado al servicio> \
  --add-cloudsql-instances <PROJECT_ID>:<region>:<instancia cloud sql> \
  --vpc-egress=all \

Ejemplo:

gcloud run deploy appdata-stg3 \
  --image gcr.io/central-apex-438817-p5/appdata-stg:latest \
  --platform managed \
  --vpc-connector projects/central-apex-438817-p5/locations/europe-west9/connectors/vpn-net-olenbee \
  --allow-unauthenticated \
  --service-account clourun-olenbee@central-apex-438817-p5.iam.gserviceaccount.com \
  --add-cloudsql-instances central-apex-438817-p5:europe-west9:olenbeedata-stg \
  --vpc-egress=all \


5. Configuración de Acceso a la Base de Datos desde la Aplicación
Para que la aplicación acceda a la base de datos de Cloud SQL, debe habilitar la conexión a Cloud SQL desde su entorno. Esto se puede hacer configurando las variables de entorno necesarias en Cloud Run o utilizando el proxy de Cloud SQL.

Asegúrese de que la instancia de Cloud SQL esté configurada para permitir conexiones desde la red de Cloud Run.