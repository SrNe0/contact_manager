# Documentación de Backend

## 1. Resumen

La capa de backend consiste en **servicios de lógica de negocio** que implementan operaciones CRUD y aplican reglas de negocio. Esta capa orquesta operaciones entre las capas de base de datos, modelos e interfaz.

## 2. Arquitectura de la Capa de Servicios

**Ubicación**: `app/services/contacts_service.py`

**Responsabilidades**:
- Implementar toda la lógica de negocio
- Coordinar entre capas
- Aplicar reglas de validación
- Generar IDs únicos
- Gestionar el ciclo de vida de contactos

## 3. Funciones de Negocio Principales

### 3.1 Generación de ID

**Función**: `generate_id(contacts)`

**Propósito**: Genera IDs de contacto únicos y secuenciales.

**Algoritmo**:
```python
def generate_id(contacts):
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1
```

**Reglas de Negocio**:
- El primer contacto obtiene ID = 1
- Los IDs subsiguientes son max(existentes) + 1
- Los IDs nunca se reutilizan después de eliminación
- Los espacios en la secuencia indican contactos eliminados

**Complejidad Temporal**: O(n)

**Ejemplo de Secuencia**:
- Inicio: `[]` → ID = 1
- Después de agregar: `[{id:1}]` → siguiente ID = 2
- Después de agregar: `[{id:1}, {id:2}]` → siguiente ID = 3
- Después de eliminar ID 1: `[{id:2}]` → siguiente ID = 3 (no 2)

### 3.2 Búsqueda de Contacto

**Función**: `find_contact_index_by_id(contacts, contact_id)`

**Propósito**: Localiza la posición de un contacto en la lista por ID.

**Algoritmo**:
```python
def find_contact_index_by_id(contacts, contact_id):
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            return index
    return -1
```

**Parámetros**:
- `contacts`: Lista de diccionarios de contacto
- `contact_id`: ID entero a buscar

**Retorna**:
- Índice (basado en 0) si se encuentra
- -1 si no se encuentra

**Complejidad Temporal**: O(n)

**Uso**: Usado por operaciones de búsqueda, actualización y eliminación

## 4. Operaciones CRUD

### 4.1 Crear Contacto

**Función**: `add_contact(contacts)`

**Historia de Usuario**: Como usuario, quiero agregar un nuevo contacto con nombre, teléfono y correo electrónico.

**Flujo de Trabajo**:
1. Mostrar encabezado de sección
2. Solicitar nombre (requerido)
3. Validar que el nombre no esté vacío
4. Solicitar teléfono (opcional, solo dígitos)
5. Solicitar correo electrónico (opcional, cualquier cadena)
6. Generar nuevo ID único
7. Crear diccionario de contacto usando capa de modelo
8. Agregar a lista de contactos
9. Guardar en archivo JSON
10. Mostrar mensaje de éxito

**Reglas de Validación**:
- Nombre: no debe estar vacío
- Teléfono: si se proporciona, debe contener solo dígitos (0-9)
- Email: sin validación (cualquier cadena aceptada)

**Manejo de Errores**:
- Nombre vacío → mostrar error, retornar lista sin cambios
- Teléfono inválido → volver a solicitar hasta que sea válido
- Fallo al guardar → mensaje de error desde capa de base de datos

**Persistencia**: Llama a `save_contacts()` después de agregar exitosamente

**Valor de Retorno**: Lista de contactos actualizada

### 4.2 Leer Todos los Contactos

**Función**: `view_all_contacts(contacts)`

**Historia de Usuario**: Como usuario, quiero ver todos mis contactos en una lista.

**Flujo de Trabajo**:
1. Mostrar encabezado de sección
2. Verificar si la lista de contactos está vacía
3. Si está vacía: mostrar "No se encontraron contactos"
4. Si no está vacía: formatear y mostrar todos los contactos
5. Retornar lista sin cambios

**Formato de Visualización**:
```
[ID] Nombre
    Teléfono: <teléfono>
    Email: <email>
```

**Ejemplo de Salida**:
```
--- TODOS LOS CONTACTOS ---

[1] John Doe
    Teléfono: 1234567890
    Email: john@example.com

[2] Jane Smith
    Teléfono: No proporcionado
    Email: jane@example.com
```

**Valor de Retorno**: Lista de contactos sin cambios (operación de solo lectura)

### 4.3 Leer Contacto Individual (Buscar)

**Función**: `search_contact(contacts)`

**Historia de Usuario**: Como usuario, quiero buscar un contacto específico por ID.

**Flujo de Trabajo**:
1. Mostrar encabezado de sección
2. Verificar si la lista de contactos está vacía
3. Solicitar ID de contacto (entero)
4. Buscar índice del contacto
5. Si no se encuentra: mostrar mensaje de error
6. Si se encuentra: formatear y mostrar detalles del contacto
7. Retornar lista sin cambios

**Formato de Visualización**:
```
ID: 1
Nombre: John Doe
Teléfono: 1234567890
Email: john@example.com
--------------------------------------------------
```

**Casos de Error**:
- Lista vacía → "No hay contactos disponibles"
- ID no encontrado → "No se encontró contacto con ID X"
- Entrada de ID inválida → volver a solicitar entero válido

**Valor de Retorno**: Lista de contactos sin cambios (operación de solo lectura)

### 4.4 Actualizar Contacto

**Función**: `update_contact(contacts)`

**Historia de Usuario**: Como usuario, quiero actualizar la información de un contacto.

**Flujo de Trabajo**:
1. Mostrar encabezado de sección
2. Verificar si la lista de contactos está vacía
3. Solicitar ID de contacto
4. Buscar índice del contacto
5. Si no se encuentra: mostrar error, retornar
6. Mostrar información actual del contacto
7. Solicitar nuevo nombre (vacío = mantener actual)
8. Si se proporciona nombre: actualizar campo de nombre
9. Solicitar nuevo teléfono (vacío = mantener actual)
10. Si se proporciona teléfono: validar y actualizar campo de teléfono
11. Solicitar nuevo email (vacío = mantener actual)
12. Si se proporciona email: actualizar campo de email
13. Guardar en archivo JSON
14. Mostrar mensaje de éxito

**Reglas de Actualización**:
- Entrada vacía → mantener valor actual
- Entrada no vacía → reemplazar valor actual
- La validación de teléfono aún aplica si se proporciona

**Ejemplo de Interacción**:
```
Ingrese nuevos valores (presione Enter para mantener actual):
Nombre: [Enter]              → mantiene nombre actual
Teléfono (solo dígitos): 999 → actualiza teléfono a "999"
Email: [Enter]               → mantiene email actual
```

**Persistencia**: Llama a `save_contacts()` después de actualización exitosa

**Valor de Retorno**: Lista de contactos actualizada

### 4.5 Eliminar Contacto

**Función**: `delete_contact(contacts)`

**Historia de Usuario**: Como usuario, quiero eliminar un contacto después de confirmar.

**Flujo de Trabajo**:
1. Mostrar encabezado de sección
2. Verificar si la lista de contactos está vacía
3. Solicitar ID de contacto
4. Buscar índice del contacto
5. Si no se encuentra: mostrar error, retornar
6. Mostrar contacto a eliminar
7. Solicitar confirmación (sí/no)
8. Si se confirma: remover de lista, guardar, mostrar éxito
9. Si no se confirma: mostrar mensaje de cancelación

**Lógica de Confirmación**:
- Aceptado: "yes", "y" (insensible a mayúsculas)
- Rechazado: cualquier otra cosa

**Ejemplo de Interacción**:
```
Contacto a eliminar:
ID: 3
Nombre: Bob Wilson
...
¿Está seguro? (yes/no): yes
Contacto 'Bob Wilson' eliminado.
```

**Persistencia**: Llama a `save_contacts()` solo si la eliminación fue confirmada

**Valor de Retorno**: Lista de contactos actualizada (o sin cambios si fue cancelada)

## 5. Reglas de Validación

### 5.1 Validación de Nombre

**Regla**: El nombre no debe estar vacío

**Capa**: Servicios

**Implementación**:
```python
name = prompt_string("Nombre: ")
if not name:
    print_error("El nombre no puede estar vacío.")
    return contacts
```

**Mensaje de Error**: "El nombre no puede estar vacío."

### 5.2 Validación de Teléfono

**Regla**: El teléfono debe contener solo dígitos (0-9)

**Capa**: Utilidades (validador reutilizable)

**Implementación**:
```python
def prompt_phone_digits(message, allow_empty):
    while True:
        phone = input(message).strip()
        if allow_empty and phone == "":
            return ""
        if phone.isdigit():
            return phone
        print("Error: El teléfono debe contener solo dígitos (0-9).")
```

**Modos**:
- Agregar contacto: `allow_empty=True` (vacío → "No proporcionado")
- Actualizar contacto: `allow_empty=True` (vacío → mantener actual)

**Mensaje de Error**: "El teléfono debe contener solo dígitos (0-9)."

### 5.3 Validación de Email

**Regla**: Sin validación (cualquier cadena aceptada)

**Justificación**: La validación de formato de email está fuera del alcance de esta versión

### 5.4 Validación de ID

**Regla**: El ID debe ser un entero válido

**Capa**: Interfaz

**Implementación**:
```python
def prompt_int(message):
    while True:
        raw = input(message).strip()
        try:
            return int(raw)
        except ValueError:
            print("Error: Por favor ingrese un entero válido.")
```

**Mensaje de Error**: "Por favor ingrese un entero válido."

## 6. Estrategia de Manejo de Errores

### 6.1 Errores de Entrada

**Estrategia**: Bucle de reintento con mensajes de error claros

**Ejemplos**:
- Entero inválido → volver a solicitar
- Teléfono inválido → volver a solicitar
- Nombre vacío → abortar operación

### 6.2 Errores de No Encontrado

**Estrategia**: Mostrar mensaje informativo y retornar

**Ejemplos**:
- ID de contacto no encontrado → "No se encontró contacto con ID X"
- Lista de contactos vacía → "No hay contactos disponibles"

### 6.3 Errores de Persistencia

**Estrategia**: Delegar a capa de base de datos

**Ejemplos**:
- Fallo al guardar → mensaje de error de `save_contacts()`
- Fallo al cargar → mensaje de error de `load_contacts()`

### 6.4 Cancelación de Usuario

**Estrategia**: Permitir salida elegante de operaciones

**Ejemplos**:
- Confirmación de eliminación rechazada → "Eliminación cancelada"
- Entrada vacía durante agregar → abortar y volver al menú

## 7. Diagramas de Flujo de Datos

Ver: [diagrams/sequence.puml](diagrams/sequence.puml)

### 7.1 Flujo de Agregar Contacto
```
Usuario → Interfaz → Servicio → Modelo → Servicio → Base de Datos
                                              → Interfaz → Usuario
```

### 7.2 Flujo de Buscar Contacto
```
Usuario → Interfaz → Servicio → [Buscar] → Helpers → Interfaz → Usuario
```

### 7.3 Flujo de Actualizar Contacto
```
Usuario → Interfaz → Servicio → [Buscar] → Interfaz → Usuario
                          ↓
                    [Actualizar] → Base de Datos
                          ↓
                     Interfaz → Usuario
```

### 7.4 Flujo de Eliminar Contacto
```
Usuario → Interfaz → Servicio → [Buscar] → Interfaz → Usuario (¿confirmar?)
                          ↓                              ↓
                    [Eliminar] ←─────────── Interfaz ← Usuario (sí)
                          ↓
                     Base de Datos
                          ↓
                     Interfaz → Usuario
```

## 8. Resumen de Reglas de Negocio

| Regla  | Descripción | Punto de Aplicación |
|--------|-------------|---------------------|
| RN-001 | El contacto debe tener un ID único | `generate_id()` |
| RN-002 | Los IDs nunca se reutilizan | `generate_id()` |
| RN-003 | El nombre es requerido | `add_contact()` |
| RN-004 | El teléfono debe ser solo dígitos si se proporciona | `prompt_phone_digits()` |
| RN-005 | Teléfono vacío → "No proporcionado" | `create_contact()` |
| RN-006 | Email vacío → "No proporcionado" | `create_contact()` |
| RN-007 | Eliminar requiere confirmación | `delete_contact()` |
| RN-008 | Entrada vacía en actualización → mantener actual | `update_contact()` |
| RN-009 | Todos los cambios se auto-guardan a JSON | Todas las operaciones mutantes |

## 9. Dependencias de Servicios

```
contacts_service.py importa:
├── app.configs.settings (constantes)
├── app.db.json_store (save_contacts)
├── app.helpers.formatters (format_contact, format_contact_list)
├── app.interface.menu (todas las funciones de E/S)
├── app.models.contact (create_contact)
└── app.utils.validators (prompt_phone_digits)
```

## 10. Consideraciones de Pruebas

### 10.1 Objetivos de Pruebas Unitarias

- `generate_id()` con lista vacía
- `generate_id()` con contactos existentes
- `generate_id()` después de eliminaciones (espacios)
- `find_contact_index_by_id()` caso encontrado
- `find_contact_index_by_id()` caso no encontrado

### 10.2 Escenarios de Pruebas de Integración

- Agregar contacto → verificar guardado en JSON
- Actualizar contacto → verificar cambios persistidos
- Eliminar contacto → verificar eliminado de JSON
- Buscar por ID inválido → verificar mensaje de error
- Operaciones con lista vacía → verificar mensajes apropiados

### 10.3 Casos Límite

- Valor máximo de ID (desbordamiento de entero)
- Caracteres Unicode en nombres
- Cadenas de entrada muy largas
- Caracteres especiales en email
- Ceros a la izquierda en números de teléfono
