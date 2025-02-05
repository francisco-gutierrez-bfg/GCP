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

# Define the entry point to run the Cloud SQL Proxy and the Spring application
ENTRYPOINT ["/bin/sh", "-c", "/cloud_sql_proxy -dir=/cloudsql -instances=central-apex-438817-p5:europe-west9:olenbeeappdata-stg=tcp:5432 & java -jar /appdata-stg.jar --spring.profiles.active=stg"]
