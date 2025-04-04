
# Ejercicio Api

## Requisitos

- Python 3 y Pip instalado
- Flask
- sqlite3 (viene por defecto en python)

---


## Recomendación


Uso de [PostMan](https://www.postman.com/) para un mejor flujo en el manejo de los endpoints.



## Instalación Flask


```bash
  pip install flask
```

## Levantar ambiente
```bash
python api.py
```


## Endpoints del Api
### Crear Incidente (POST)

La creación de inidentes debe ser en formato JSON.  Ejemplo del Body:

``` bash
{
  "reporter": "Juan Pérez",
  "description": "No funciona el teclado.",
  "status": "pendiente" 
}

```
Ruta a solicitar el metodo POST:

``` bash
ip:puerto/incidents

```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Id` | `number` | **AUTOGENERADO**. No se necesita ingresar un id |
| `reporter` | `string` | Nombre del usuario que reporta el incidente. |
| `description ` | `string` | Descripción del problema. |
| `status ` | `string` |  pendiente, en proceso, resuelto. |
| `created_at  ` | `string` | **AUTOGENERADO**. No se necesita ingresar fecha de reporte. |

**NOTA:** Para el parametro de status, escribir los estados tal y como se muestra en la tabla, de no hacerlo puede generar errores (Es decir, en minusculas).


### Obtener todos los incidentes (GET)

Hacer request a la siguiente URL donde traerá todos los incidentes existentes:

``` bash
ip:puerto/incidents

```



### Obtener icnidente en especifico (GET/{id})

Hacer request a la siguiente URL donde traerá el incidente con el id especificado:

``` bash
ip:puerto/incidents/<id>

```

### Actualizar incidente (PUT)

Para acutalizar se necesita realizar una peticion put a la siguiente URL con el ID del incidente a actualizar.

``` bash
ip:puerto/incidents/<id>

```
y un body en formato Json con los datos a actualizar:



``` bash
{
  "status": "resuelto"
}

```



### Eliminar incidente (DELETE)

Para eliminar  se necesita realizar una peticion Delete a la siguiente URL con el ID del incidente a eliminar.

``` bash
ip:puerto/incidents/<id>

```
y un body en formato Json con los datos a actualizar:



``` bash
{
  "status": "resuelto"
}

```
