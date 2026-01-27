# Documentación de Base de Datos

## 1. Resumen

El Contact Manager utiliza una **capa de persistencia basada en archivos
JSON** en lugar de una base de datos tradicional. Este enfoque
proporciona simplicidad, portabilidad y cero dependencias externas
mientras cumple con los requisitos de la aplicación.

## 2. Tecnología de Almacenamiento

**Tecnología**: JSON (JavaScript Object Notation)

**Ubicación del Archivo**: `contacts.json` (directorio raíz)

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
        "phone": "No proporcionado",
        "email": "jane@example.com"
    }
]
```

### 3.2 Esquema de Contacto

| Campo | Tipo    | Requerido | Restricciones         | Valor Predeterminado |
|-------|---------|-----------|------------------------|----------------------|
| id    | entero  | Sí        | Único, positivo        | auto-generado        |
| name  | cadena  | Sí        | No vacío               | N/A                  |
| phone | cadena  | No        | Solo dígitos o vacío   | "No proporcionado"   |
| email | cadena  | No        | Cualquier cadena       | "No proporcionado"   |

### 3.3 Descripción de Campos

**id**:

- Identificador único para cada contacto
- Generado usando estrategia max(ids_existentes) + 1
- Nunca reutilizado incluso después de eliminación
- Tipo: entero positivo comenzando desde 1

**name**:

- Nombre completo del contacto
- No puede estar vacío (validado en la entrada)
- Tipo: cadena
- Sin restricciones de longitud

**phone**:

- Número de teléfono del contacto
- Almacenado como cadena para preservar ceros a la izquierda
- Debe contener solo dígitos (0-9) si se proporciona
- Almacenado como "No proporcionado" si se deja vacío
- Tipo: cadena

**email**:

- Dirección de correo electrónico del contacto
- Sin validación de formato aplicada
- Almacenado como "No proporcionado" si se deja vacío
- Tipo: cadena

## 4. Operaciones de Base de Datos

### 4.1 Cargar Contactos

**Función**: `load_contacts()`

**Ubicación**: `app/db/json_store.py`

**Algoritmo**:

1. Verificar si `contacts.json` existe
2. Si no existe: retornar lista vacía `[]`
3. Si existe: abrir archivo y parsear JSON
4. Validar que el elemento raíz sea un arreglo
5. Retornar arreglo de diccionarios de contacto

**Manejo de Errores**:

- Archivo faltante → retorna `[]`
- JSON inválido → imprime error, retorna `[]`
- Raíz no es arreglo → imprime advertencia, retorna `[]`
- Error de permisos → imprime error, retorna `[]`

**Rendimiento**: O(n) donde n = número de contactos

### 4.2 Guardar Contactos

**Función**: `save_contacts(contacts)`

**Ubicación**: `app/db/json_store.py`

**Algoritmo**:

1. Abrir `contacts.json` para escritura
2. Serializar lista de contactos a JSON con indentación
3. Escribir al archivo con codificación UTF-8
4. Retornar estado de éxito

**Parámetros**:

- `contacts`: Lista de diccionarios de contacto

**Retorna**: Booleano (True si exitoso, False de lo contrario)

**Manejo de Errores**:

- Error de escritura → imprime error, retorna False
- Error de permisos → imprime error, retorna False

**Rendimiento**: O(n) donde n = número de contactos

**Formato JSON**:

- Indentación de 4 espacios para legibilidad
- Codificación UTF-8 con `ensure_ascii=False` para caracteres
internacionales
- Formato embellecido para edición manual

## 5. Justificación de JSON vs Base de Datos

### 5.1 ¿Por qué JSON?

**Ventajas**:

1. **Cero Dependencias**: No se requiere instalación de servidor de base
de datos o driver
2. **Portabilidad**: Un solo archivo puede copiarse, respaldarse o
versionarse
3. **Legible por Humanos**: Los archivos JSON pueden editarse e
inspeccionarse manualmente
4. **Simplicidad**: Sin migraciones de esquema, sin gestión de
conexiones
5. **Ligero**: Perfecto para conjuntos de datos pequeños a medianos
(< 10,000 registros)
6. **Biblioteca Estándar**: El módulo `json` de Python está integrado y
es confiable

**Compromisos Aceptados**:

1. **Sin Acceso Concurrente**: Múltiples usuarios no pueden editar
simultáneamente
2. **Cargar Todo o Nada**: El archivo completo se carga en memoria
3. **Sin Indexación**: La búsqueda requiere escaneo lineal
4. **Sin Relaciones**: Sin claves foráneas o joins
5. **Bloqueo de Archivos**: Sin soporte de transacciones integrado

### 5.2 Cuándo Este Enfoque Es Apropiado

Este enfoque basado en JSON es apropiado cuando:

- La base de usuarios es de un solo usuario o equipo pequeño
- El tamaño del conjunto de datos es menor a 100,000 registros
- No se requiere acceso de escritura concurrente
- La portabilidad es más importante que el rendimiento
- Cero dependencias externas es un requisito

### 5.3 Ruta de Migración

Si la aplicación necesita escalar, la capa de base de datos puede
reemplazarse:

1. Crear nuevo módulo: `app/db/sql_store.py`
2. Implementar la misma interfaz: `load_contacts()`, `save_contacts()`
3. Actualizar imports en `app/main.py`
4. La capa de servicios no requiere cambios

## 6. Integridad de Datos

### 6.1 Unicidad de ID

**Estrategia**: Max + 1

**Algoritmo**:

```python
def generate_id(contacts):
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1
```

**Garantías**:

- Los IDs son siempre únicos
- Los IDs nunca se reutilizan después de eliminación
- Los IDs son secuenciales (con espacios después de eliminaciones)

### 6.2 Validación de Datos

**En Entrada**:

- Nombre: requerido, no vacío (validado por interfaz)
- Teléfono: solo dígitos si se proporciona (validado por interfaz)
- Email: sin validación (aceptado tal cual)

**En Almacenamiento**:

- Sin validación adicional (confiar en la capa de servicio)
- La normalización aplica valores predeterminados ("No proporcionado")

### 6.3 Respaldo y Recuperación

**Respaldo Manual**:

```bash
cp contacts.json contacts.backup.json
```

**Recuperación de Corrupción**:

- La aplicación detecta JSON inválido
- Comienza con lista de contactos vacía
- Muestra mensaje de error al usuario
- El usuario puede restaurar desde respaldo manualmente

## 7. Características de Rendimiento

| Operación        | Complejidad Temporal | Complejidad Espacial |
|------------------|----------------------|----------------------|
| Cargar Todo      | O(n)                 | O(n)                 |
| Guardar Todo     | O(n)                 | O(n)                 |
| Buscar por ID    | O(n)                 | O(1)                 |
| Agregar Contacto | O(1) + O(n)          | O(n)                 |
| Actualizar       | O(n) + O(n)          | O(n)                 |
| Eliminar         | O(n) + O(n)          | O(n)                 |

| Operación        | Notas                       |
|------------------|-----------------------------|
| Cargar Todo      | Parsea JSON completo        |
| Guardar Todo     | Serializa lista completa    |
| Buscar por ID    | Búsqueda lineal en memoria  |
| Agregar Contacto | Agregar + guardar           |
| Actualizar       | Buscar + guardar            |
| Eliminar         | Buscar + remover + guardar  |

**Cuello de Botella**: E/S de archivo durante operaciones de guardado

**Optimización**: Las operaciones de guardado podrían ser diferidas o
agrupadas para múltiples cambios

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
        "phone": "No proporcionado",
        "email": "bob@work.com"
    },
    {
        "id": 5,
        "name": "Carol Martínez",
        "phone": "5559876543",
        "email": "No proporcionado"
    }
]
```

**Nota**: Los IDs 3 y 4 faltantes indican contactos eliminados (los IDs
nunca se reutilizan)

## 9. Ubicación y Nombre del Archivo

**Nombre del Archivo**: `contacts.json`

**Ubicación**: Directorio raíz de la aplicación (mismo nivel que la
carpeta `app/`)

**Justificación**:

- Ubicación simple y predecible
- Fácil de encontrar para respaldo
- Compatible con control de versiones (puede ser .gitignored)

## 10. Codificación de Caracteres

**Codificación**: UTF-8

**Por qué**: Soporta caracteres internacionales en nombres y correos
electrónicos

**Implementación**:

```python
with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
    # Operación de lectura

with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(contacts, file, indent=4, ensure_ascii=False)
```
