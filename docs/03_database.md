# Documentación de Base de Datos

## 1. Resumen

El Contact Manager utiliza una **capa de persistencia basada en archivos
JSON** en lugar de una base de datos tradicional. Este enfoque
proporciona simplicidad, portabilidad y cero dependencias externas
mientras cumple con los requisitos de la aplicación.

## 2. Tecnología de Almacenamiento

**Tecnología**: JSON (JavaScript Object Notation)

**Ubicación del Archivo**: `contacts.json` (raíz del proyecto)

**Método de Acceso**: Módulo `json` de la biblioteca estándar de Python

## 3. Estructura de Datos

### 3.1 Formato del Archivo

El archivo JSON contiene un único arreglo de objetos de contacto:

```json
[
    {
        "id": 1,
        "name": "John Doe",
        "phone": "1234567890",
        "email": "john@example.com"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "phone": "Not provided",
        "email": "jane@example.com"
    }
]
```

### 3.2 Esquema de Contacto

| Campo | Tipo   | Requerido | Restricciones             | Valor Predeterminado |
|-------|--------|-----------|---------------------------|----------------------|
| id    | entero | Sí        | Único, positivo           | auto-generado        |
| name  | cadena | Sí        | No vacío                  | N/A                  |
| phone | cadena | No        | Solo dígitos 0-9          | "Not provided"       |
| email | cadena | No        | Forma `nombre@dominio.tld` | "Not provided"      |

### 3.3 Descripción de Campos

**id**:

- Identificador único para cada contacto
- Generado usando la estrategia max(ids_existentes) + 1
- Tipo: entero positivo comenzando desde 1

**name**:

- Nombre completo del contacto
- No puede estar vacío
- Tipo: cadena
- Sin restricciones de longitud

**phone**:

- Número de teléfono del contacto
- Almacenado como cadena para preservar ceros a la izquierda
- Debe contener solo dígitos (0-9) si se ingresa
- Almacenado como "Not provided" si se deja vacío
- Tipo: cadena

**email**:

- Dirección de correo electrónico del contacto
- Debe tener la forma `nombre@dominio.tld` si se ingresa
- Almacenado como "Not provided" si se deja vacío
- Tipo: cadena

Las reglas de formato se aplican a lo que el usuario ingresa. Un valor
existente en el archivo se conserva aunque no cumpla el formato actual.

## 4. Operaciones de Base de Datos

### 4.1 Cargar Contactos

**Función**: `load_contacts(path=JSON_FILE_PATH)`

**Ubicación**: `app/db/json_store.py`

**Retorna**: Tupla `(contactos, advertencia)`. La advertencia es `None`
si no hubo problemas.

| Situación | Resultado |
|-----------|-----------|
| El archivo no existe | Lista vacía, sin advertencia |
| JSON válido con registros correctos | Lista de contactos, sin advertencia |
| Faltan campos opcionales, o el ID falta, es inválido o está repetido | Se repara al cargar, sin advertencia |
| Algunos registros no son recuperables (sin nombre o no son objetos) | Respaldo del original, se guardan los válidos y se advierte |
| JSON inválido, codificación inválida o raíz que no es un arreglo | Respaldo del original, lista vacía y advertencia |
| El archivo no se puede leer, respaldar o reparar | Lanza `OSError`; la aplicación se cierra |

**Rendimiento**: O(n) donde n = número de contactos

### 4.2 Guardar Contactos

**Función**: `save_contacts(contacts, path=JSON_FILE_PATH)`

**Ubicación**: `app/db/json_store.py`

**Algoritmo**:

1. Serializar la lista completa a texto JSON
2. Escribirla en un archivo temporal en el mismo directorio
3. Forzar la escritura a disco con `os.fsync`
4. Reemplazar `contacts.json` con `os.replace`, una operación atómica
5. Si algo falla: eliminar el temporal y relanzar la excepción

**Garantía**: `contacts.json` siempre contiene la versión anterior completa
o la nueva completa, nunca una escritura parcial.

**Manejo de Errores**: Lanza `OSError`. El flujo que la llamó muestra el
error y conserva la lista anterior.

**Rendimiento**: O(n) donde n = número de contactos

**Formato JSON**:

- Indentación de 4 espacios para legibilidad
- Codificación UTF-8 con `ensure_ascii=False` para caracteres
internacionales

### 4.3 Exportar a CSV

**Función**: `export_contacts_csv(contacts, path=CSV_EXPORT_PATH)`

**Ubicación**: `app/db/csv_export.py`

**Formato**:

- Archivo `contacts_export.csv` en la raíz del proyecto; cada exportación
reemplaza a la anterior
- Columnas: `id`, `name`, `phone`, `email`
- UTF-8 con BOM, para que Excel muestre bien los acentos
- El texto que empieza con `=`, `+`, `-`, `@`, tabulación o retorno de carro
se antepone con `'`, para que una hoja de cálculo no lo ejecute como fórmula

## 5. Justificación de JSON vs Base de Datos

### 5.1 ¿Por qué JSON?

**Ventajas**:

1. **Cero Dependencias**: No se requiere instalación de servidor de base
de datos o driver
2. **Portabilidad**: Un solo archivo puede copiarse o respaldarse
3. **Legible por Humanos**: Los archivos JSON pueden editarse e
inspeccionarse manualmente
4. **Simplicidad**: Sin migraciones de esquema, sin gestión de
conexiones
5. **Ligero**: Perfecto para conjuntos de datos pequeños a medianos
(< 10,000 registros)
6. **Biblioteca Estándar**: El módulo `json` de Python está integrado y
es confiable

**Compromisos Aceptados**:

1. **Sin Acceso Concurrente**: Si dos procesos escriben, gana el último
2. **Cargar Todo o Nada**: El archivo completo se carga en memoria
3. **Sin Indexación**: La búsqueda requiere escaneo lineal
4. **Sin Relaciones**: Sin claves foráneas o joins

### 5.2 Cuándo Este Enfoque Es Apropiado

Este enfoque basado en JSON es apropiado cuando:

- La aplicación tiene un solo usuario
- El tamaño del conjunto de datos es menor a 100,000 registros
- No se requiere acceso de escritura concurrente
- La portabilidad es más importante que el rendimiento
- Cero dependencias externas es un requisito

### 5.3 Ruta de Migración

Si la aplicación necesita escalar, la capa de base de datos puede
reemplazarse:

1. Crear nuevo módulo: `app/db/sql_store.py`
2. Implementar las mismas funciones: `load_contacts()`, `save_contacts()`
3. Actualizar imports en `app/main.py` y `app/interface/contact_flows.py`
4. La capa de servicios no requiere cambios

## 6. Integridad de Datos

### 6.1 Unicidad de ID

**Estrategia**: Max + 1

**Algoritmo**:

```python
def generate_id(contacts):
    return max((contact["id"] for contact in contacts), default=0) + 1
```

**Garantías**:

- Un ID nuevo nunca coincide con el de un contacto existente
- Los IDs pueden tener espacios después de eliminaciones
- Si se elimina el contacto con el ID más alto, ese ID se puede volver a
asignar, porque el formato del archivo no guarda un historial de IDs

### 6.2 Validación de Datos

**En Entrada**:

- Nombre: requerido, no vacío
- Teléfono: solo dígitos 0-9 si se ingresa
- Email: forma `nombre@dominio.tld` si se ingresa

**Al Cargar**:

- `normalize_contacts()` completa campos opcionales y repara IDs
- Los registros sin nombre válido se descartan, con respaldo del original

### 6.3 Respaldo y Recuperación

**Respaldo Automático**: Un archivo dañado se mueve a
`contacts.json.corrupt-AAAAMMDD-HHMMSS` en la misma carpeta.

**Recuperación**: Corrija el respaldo con un editor y cámbiele el nombre a
`contacts.json` con la aplicación cerrada.

**Respaldo Manual**:

```bash
cp contacts.json contacts.backup.json
```

## 7. Características de Rendimiento

| Operación        | Complejidad Temporal | Complejidad Espacial |
|------------------|----------------------|----------------------|
| Cargar Todo      | O(n)                 | O(n)                 |
| Guardar Todo     | O(n)                 | O(n)                 |
| Buscar por ID    | O(n)                 | O(1)                 |
| Buscar por texto | O(n)                 | O(n)                 |
| Agregar Contacto | O(n)                 | O(n)                 |
| Actualizar       | O(n)                 | O(n)                 |
| Eliminar         | O(n)                 | O(n)                 |

**Cuello de Botella**: E/S de archivo durante operaciones de guardado

## 8. Ejemplo de Archivo JSON

**Base de Datos Vacía**:

```json
[]
```

**Base de Datos con Tres Contactos**:

```json
[
    {
        "id": 1,
        "name": "Alice Johnson",
        "phone": "5551234567",
        "email": "alice@example.com"
    },
    {
        "id": 2,
        "name": "Bob Wilson",
        "phone": "Not provided",
        "email": "bob@work.com"
    },
    {
        "id": 5,
        "name": "Carol Martínez",
        "phone": "5559876543",
        "email": "Not provided"
    }
]
```

**Nota**: Los IDs 3 y 4 faltantes indican contactos eliminados.

## 9. Ubicación y Nombre del Archivo

**Nombre del Archivo**: `contacts.json`

**Ubicación**: Raíz del proyecto (mismo nivel que la carpeta `app/`). La
ruta se calcula con `pathlib` desde `settings.py`, así que no depende del
directorio de ejecución.

**Control de Versiones**: `contacts.json`, sus respaldos y
`contacts_export.csv` están en `.gitignore`, porque contienen datos
personales.

## 10. Codificación de Caracteres

**Codificación**: UTF-8

**Por qué**: Soporta caracteres internacionales en nombres y correos
electrónicos

**Implementación**: `json.load` lee con `encoding="utf-8"` y `save_contacts`
escribe con `encoding="utf-8"` y `ensure_ascii=False`.
