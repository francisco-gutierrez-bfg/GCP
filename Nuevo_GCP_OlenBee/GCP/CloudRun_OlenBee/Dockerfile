FROM ubuntu:latest

# OS update and package installation process
RUN apt update \
  && apt-get -y install openjdk-8-jdk wget \
  && mkdir /usr/local/tomcat \
  && wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.96/bin/apache-tomcat-9.0.96.tar.gz -O /tmp/tomcat.tar.gz \
  && cd /tmp && tar xvfz tomcat.tar.gz \
  && mv /tmp/apache-tomcat-9.0.96 /tmp/tomcat \
  && cp -Rv /tmp/tomcat/* /usr/local/tomcat/ \
  && rm -rf /tmp/tomcat \
  # Cleanup apt
  ###
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Descargar el proxy de Cloud SQL
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /cloud_sql_proxy
RUN chmod +x /cloud_sql_proxy 

# Copiar el archivo de app de test WAR
ADD settings/sample.war /usr/local/tomcat/webapps/

# Desplegar la app
COPY settings/appdata-stg.war /usr/local/tomcat/webapps/

# Copiar archivos de configuración (si es necesario)
COPY settings/tomcat-users.xml /usr/local/tomcat/conf/
COPY settings/context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml 
COPY settings/manager.xml /usr/local/tomcat/conf/ 

# Exponer el puerto 8080
EXPOSE 8080

# Comando de inicio
#CMD ["/bin/sh", "-c", "/cloud_sql_proxy -dir=/cloudsql -instances=central-apex-438817-p5:europe-west9:olenbeeappdata-stg=tcp:5432 & catalina.sh run"]
CMD ["/bin/sh", "-c", "/cloud_sql_proxy -dir=/cloudsql -instances=central-apex-438817-p5:europe-west9:olenbeeappdata-stg=tcp:5432 & /usr/local/tomcat/bin/catalina.sh run"]
