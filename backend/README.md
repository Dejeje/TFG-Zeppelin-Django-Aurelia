# Comandos de Docker Compose

## Iniciar los servicios definidos en el archivo docker-compose.yml


```
docker-compose up
```

Esta opción se puede lanzar en background e indicarle a docker que construya las imagenes

```
docker-compose up -d --build
```

## Detener los servicios en ejecución

```
docker-compose down
```

## Construir las imágenes y luego iniciar los servicios

```
docker-compose up --build
```

## Ver los logs de los servicios en ejecución

```
docker logs <NOMBRE_CONTENEDOR>
```

## Ver el estado de los servicios

```
docker ps
```

## Ejecutar comandos en un servicio en ejecución

```
docker exec -it <NOMBRE_CONTENEDOR> <COMANDO>
```

Por ejemplo:
```
docker exec -it backend sh
```

Este comando ejecuta una terminal de bash en el contenedor, por lo que nos conectamos al contenedor y podemos hacer las modificaciones que queramos desde dentro.

## Detener y eliminar los contenedores, redes y volúmenes asociados a los servicios

```
docker-compose down --volumes
```

## Migraciones

Pasos:

1. Entramos al contenedor:
    ```
    docker exec -it backend sh
    ```
2. Creamos migraciones con nuevos cambios, si no hay cambios saltamos este paso
   ```
    # python manage.py makemigrations
    ```
3. Ejecutamos las migraciones
   ```
    # python manage.py migrate  
    ```