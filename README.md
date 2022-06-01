# Challenge mi Aguila

## Se implementa la siguiente arquitectura de microservicios para resolver el challenge

![alt text](docs/images/challenge.drawio.png)

### Prerequisitos

```
docker
docker-compose
```

### Instalación y configuración

git clone https://github.com/choucoder/challenge.git
cd challenge

#### Servicio 1

cd fileupload
sudo docker-compose up

##### En otra terminal realizar migraciones para tablas de MYSQL

sudo docker-compose exec backend sh
python manage.py makemigrations
python manage.py migrate

#### Servicio 2

cd postcodes
sudo ip addr show docker0
colocar la ip de la interfaz docker0 en el archivo .env, y luego
sudo docker-compose up

### Ejecutar pruebas

#### Servicio 1

python manage.py test apps

#### Servicio 2

pytest tests.py
