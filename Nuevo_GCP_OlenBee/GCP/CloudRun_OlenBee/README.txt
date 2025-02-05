A continuación se presenta un ejemplo de un Dockerfile para crear un contenedor de Tomcat que se conecta a una base de datos de Cloud SQL. También se incluye la configuración de server.xml, instrucciones para el acceso a la base de datos desde la aplicación, y pasos para desplegar en Cloud Run.

1. Dockerfile

# Utilizar la imagen base de Tomcat
FROM tomcat:9.0

# Instalar el driver JDBC de PostgreSQL
RUN apt-get update && apt-get install -y wget \
    && wget https://jdbc.postgresql.org/download/postgresql-42.3.1.jar -P /usr/local/tomcat/lib/ \
    && apt-get clean

# Copiar la aplicación .war al contenedor
COPY ./mi-aplicacion.war /usr/local/tomcat/webapps/

# Copiar la configuración de Tomcat
COPY ./server.xml /usr/local/tomcat/conf/

# Exponer el puerto
EXPOSE 8080

# Comando para iniciar Tomcat
CMD ["catalina.sh", "run"]

2. Configuración de server.xml
Asegúrese de modificar el archivo server.xml según sus necesidades. A continuación se muestra un ejemplo básico que incluye la configuración para conectarse a una base de datos de Cloud SQL:


<Server port="8005" shutdown="SHUTDOWN">
    <Service name="Catalina">
        <Connector port="8080" protocol="HTTP/1.1"
                   connectionTimeout="20000"
                   redirectPort="8443" />
        
        <Engine name="Catalina" defaultHost="localhost">
            <Host name="localhost" appBase="webapps"
                  unpackWARs="true" autoDeploy="true">
                <Context path="/mi-aplicacion" docBase="mi-aplicacion.war" />
                
                <!-- Configuración de la conexión a la base de datos -->
                <Resource name="jdbc/miDB"
                          auth="Container"
                          type="javax.sql.DataSource"
                          driverClassName="org.postgresql.Driver"
                          url="jdbc:postgresql://<CLOUD_SQL_CONNECTION_NAME>/<DB_NAME>"
                          username="<DB_USERNAME>"
                          password="<DB_PASSWORD>"
                          maxTotal="20"
                          maxIdle="10"
                          maxWaitMillis="-1"/>
            </Host>
        </Engine>
    </Service>
</Server>

3. Configuración de la Aplicación
Asegúrese de que su aplicación Java esté configurada para utilizar el recurso JNDI para conectarse a la base de datos. Aquí hay un ejemplo de cómo se puede obtener una conexión desde la aplicación:

Context initContext = new InitialContext();
Context envContext = (Context) initContext.lookup("java:comp/env");
DataSource ds = (DataSource) envContext.lookup("jdbc/miDB");
Connection conn = ds.getConnection();

4. Instrucciones para Despliegue en Cloud Run

Autenticarse en GCP:

gcloud auth login
gcloud config set project <PROJECT_ID>
Construir la imagen de Docker:


docker build -t gcr.io/<YOUR_PROJECT_ID>/mi-aplicacion .

Subir la imagen al Container Registry:

docker push gcr.io/<YOUR_PROJECT_ID>/mi-aplicacion

Desplegar en Cloud Run:

gcloud run deploy mi-aplicacion \
    --image gcr.io/<PROJECT_ID>/mi-aplicacion \
    --platform managed \
    --region <REGION> \
    --allow-unauthenticated

5. Configuración de Acceso a la Base de Datos desde la Aplicación
Para que la aplicación acceda a la base de datos de Cloud SQL, debe habilitar la conexión a Cloud SQL desde su entorno. Esto se puede hacer configurando las variables de entorno necesarias en Cloud Run o utilizando el proxy de Cloud SQL.

Asegúrese de que la instancia de Cloud SQL esté configurada para permitir conexiones desde la red de Cloud Run.