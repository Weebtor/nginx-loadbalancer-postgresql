# nginx-loadbalancer-postgresql
Implementación de balanceador de carga con Nginx y replicas de bases de datos, para un microservicio de un inventario

Update


Docker

docker run -dti -p 55432:5432 --name postgresql-master \
  -e POSTGRESQL_REPLICATION_MODE=master \
  -e POSTGRESQL_USERNAME=zuka \
  -e POSTGRESQL_PASSWORD=zukaritas \
  -e POSTGRESQL_DATABASE=my_database \
  -e POSTGRESQL_REPLICATION_USER=zukas \
  -e POSTGRESQL_REPLICATION_PASSWORD=zucaritas \
  bitnami/postgresql:latest

docker run -dti -p 65432:5432 --name postgresql-slave \
  --link postgresql-master:master \
  -e POSTGRESQL_REPLICATION_MODE=slave \
  -e POSTGRESQL_USERNAME=zuka \
  -e POSTGRESQL_PASSWORD=zukaritas \
  -e POSTGRESQL_MASTER_HOST=master \
  -e POSTGRESQL_MASTER_PORT_NUMBER=5432 \
  -e POSTGRESQL_REPLICATION_USER=zukas \
  -e POSTGRESQL_REPLICATION_PASSWORD=zucaritas \
  bitnami/postgresql:latest

export FLASK_APP=./src/flask_app.py
flask run -h localhost -p 2000


{
    "nombre":"MIRA",
    "codigo":"TEST02",
    "precio": 500000000.6
}

192.168.1.195/GetProduct?q=aa

192.168.1.195/AddProduct