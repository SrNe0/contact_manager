# Documentación de Arquitectura

## 1. Resumen

La aplicación Contact Manager sigue un patrón de **arquitectura en capas** que separa las responsabilidades en capas distintas. Cada capa tiene una responsabilidad específica y se comunica solo con las capas adyacentes.

Esta arquitectura promueve:
- **Separación de Responsabilidades**: Cada capa maneja un aspecto específico de la aplicación
- **Mantenibilidad**: Los cambios en una capa tienen impacto mínimo en otras
- **Testeabilidad**: Cada capa puede ser probada independientemente
- **Legibilidad**: La organización clara hace que la base de código sea fácil de entender

## 2. Diagrama de Arquitectura

Ver: [diagrams/architecture.png](diagrams/architecture.png)

## 3. Descripción de Capas

### 3.1 Capa de Configuración (`app/configs/`)

**Propósito**: Configuración centralizada de la aplicación y constantes.

**Responsabilidades**:
- Definir todos los números mágicos como constantes con nombre
- Almacenar rutas de archivos y valores de configuración
- Proporcionar configuraciones a nivel de aplicación

**Archivos**:
- `settings.py`: Todas las constantes (MENU_WIDTH, JSON_FILE_PATH, EXIT_OPTION, etc.)

**Dependencias**: Ninguna (capa inferior)

**Constantes Clave**:
- `MENU_WIDTH`: Ancho de la visualización del menú (50 caracteres)
- `MENU_MIN_OPTION`, `MENU_MAX_OPTION`: Rango de opciones válidas del menú
- `EXIT_OPTION`: Número de opción del menú para salir (6)
- `NOT_PROVIDED`: Valor predeterminado para campos opcionales
- `CONFIRM_YES_VALUES`: Entradas de confirmación aceptadas
- `JSON_FILE_PATH`: Ruta al archivo JSON de contactos

### 3.2 Capa de Modelos (`app/models/`)

**Propósito**: Definiciones de estructura de datos y normalización.

**Responsabilidades**:
- Definir la estructura de datos del contacto (como diccionarios)
- Proporcionar funciones de fábrica para crear contactos
- Normalizar datos de contacto de fuentes externas

**Archivos**:
- `contact.py`: Funciones de creación y normalización de contactos

**Dependencias**: Capa de configuración

**Funciones Clave**:
- `create_contact(id, name, phone, email)`: Crea un diccionario de contacto
- `normalize_contact(contact)`: Asegura que el contacto tenga todos los campos requeridos

**Decisión de Diseño**: Usa diccionarios en lugar de clases para cumplir con el requisito de programación funcional.

### 3.3 Capa de Base de Datos (`app/db/`)

**Propósito**: Persistencia y recuperación de datos.

**Responsabilidades**:
- Cargar contactos desde archivo JSON
- Guardar contactos en archivo JSON
- Manejar errores de E/S de archivos de manera elegante
- Validar estructura JSON

**Archivos**:
- `json_store.py`: Operaciones de archivo JSON

**Dependencias**: Capa de configuración

**Funciones Clave**:
- `load_contacts()`: Lee contactos del archivo JSON, retorna lista
- `save_contacts(contacts)`: Escribe contactos al archivo JSON, retorna booleano de éxito

**Manejo de Errores**:
- Archivo faltante: Retorna lista vacía
- JSON inválido: Imprime error, retorna lista vacía
- Errores de permisos de archivo: Imprime error, retorna lista vacía o False

### 3.4 Capa de Utilidades (`app/utils/`)

**Propósito**: Funciones de utilidad reutilizables.

**Responsabilidades**:
- Operaciones de consola (limpiar pantalla)
- Validación de entrada (números de teléfono)
- Funciones auxiliares genéricas

**Archivos**:
- `console.py`: Funciones de manipulación de consola
- `validators.py`: Funciones de validación de entrada

**Dependencias**: Ninguna (capa de utilidad)

**Funciones Clave**:
- `clear_screen()`: Limpia el terminal usando códigos ANSI
- `prompt_phone_digits(message, allow_empty)`: Valida entrada de teléfono

### 3.5 Capa de Helpers (`app/helpers/`)

**Propósito**: Helpers de formato y visualización.

**Responsabilidades**:
- Formatear contactos para visualización
- Generar cadenas de visualización
- Manejar lógica de presentación

**Archivos**:
- `formatters.py`: Funciones de formato de contactos

**Dependencias**: Capa de configuración

**Funciones Clave**:
- `format_contact(contact)`: Formatea un contacto individual para visualización
- `format_contact_list(contacts)`: Formatea lista de contactos para visualización

### 3.6 Capa de Interfaz (`app/interface/`)

**Propósito**: Interacción con el usuario y entrada/salida.

**Responsabilidades**:
- Mostrar menús y mensajes
- Leer entrada del usuario
- Imprimir mensajes y errores
- Manejar el flujo de interacción del usuario

**Archivos**:
- `menu.py`: Funciones de visualización de menú y entrada

**Dependencias**: Capa de configuración

**Funciones Clave**:
- `show_menu()`: Muestra el menú principal
- `prompt_menu_option()`: Obtiene selección del menú
- `prompt_string(message)`: Obtiene entrada de cadena
- `prompt_int(message)`: Obtiene entrada de entero validada
- `prompt_confirmation(message)`: Obtiene confirmación sí/no
- `wait_for_enter()`: Pausa para reconocimiento del usuario
- `print_message(message)`: Muestra información
- `print_error(message)`: Muestra error

**Principio de Diseño**: Esta capa no sabe nada sobre lógica de negocio; solo maneja E/S.

### 3.7 Capa de Servicios (`app/services/`)

**Propósito**: Lógica de negocio y operaciones CRUD.

**Responsabilidades**:
- Implementar todas las reglas de negocio
- Orquestar operaciones entre capas
- Generar IDs únicos
- Encontrar contactos por ID
- Coordinar operaciones de crear, leer, actualizar, eliminar

**Archivos**:
- `contacts_service.py`: Lógica de negocio de contactos

**Dependencias**: Todas las capas inferiores (base de datos, modelos, interfaz, helpers, utils, config)

**Funciones Clave**:
- `generate_id(contacts)`: Crea ID único usando estrategia max+1
- `find_contact_index_by_id(contacts, id)`: Localiza contacto en la lista
- `add_contact(contacts)`: Maneja flujo de trabajo de creación de contacto
- `view_all_contacts(contacts)`: Muestra todos los contactos
- `search_contact(contacts)`: Busca y muestra contacto por ID
- `update_contact(contacts)`: Maneja flujo de trabajo de actualización de contacto
- `delete_contact(contacts)`: Maneja eliminación de contacto con confirmación

**Reglas de Negocio**:
- Los IDs son siempre únicos y secuenciales
- El teléfono debe ser solo dígitos si se proporciona
- El nombre es obligatorio
- Entrada vacía durante actualización significa "mantener valor actual"
- Eliminar requiere confirmación explícita

### 3.8 Capa de Aplicación (`app/main.py`)

**Propósito**: Punto de entrada de la aplicación y bucle principal.

**Responsabilidades**:
- Inicializar la aplicación
- Cargar datos iniciales
- Ejecutar bucle de eventos principal
- Enrutar selecciones de menú a servicios
- Manejar ciclo de vida de la aplicación

**Dependencias**: Servicios, Interfaz, Utilidades, Base de Datos

**Funciones Clave**:
- `main()`: Bucle principal de la aplicación

**Flujo de Control**:
1. Cargar contactos desde JSON
2. Mostrar mensaje de bienvenida
3. Bucle:
   - Limpiar pantalla
   - Mostrar menú
   - Obtener opción del usuario
   - Si salir: romper
   - Si inválida: mostrar error
   - Si válida: ejecutar función de servicio
   - Esperar Enter
4. Mostrar mensaje de despedida

## 4. Flujo de Datos

### 4.1 Flujo de Operación de Lectura
```
Usuario → Interfaz → Servicios → Base de Datos → Archivo JSON
                                   ↓
Usuario ← Interfaz ← Helpers ← Servicios ← (lista de contactos)
```

### 4.2 Flujo de Operación de Escritura
```
Usuario → Interfaz → Servicios → Modelos → (nuevo contacto)
                       ↓
                   Base de Datos → Archivo JSON
                       ↓
Usuario ← Interfaz ← Servicios
```

Ver: [diagrams/sequence.puml](diagrams/sequence.puml)

## 5. Reglas de Dependencia

1. **Solo Dependencias Descendentes**: Las capas superiores dependen de las inferiores, nunca al revés
2. **Sin Acceso Entre Capas**: Los servicios no pueden llamar directamente a la Base de Datos sin pasar por la interfaz definida
3. **Responsabilidad Única**: Cada módulo tiene una razón para cambiar

## 6. Matriz de Interacción de Capas

| Capa        | Puede Usar                                    |
|-------------|-----------------------------------------------|
| Main        | Services, Interface, Utils, Database          |
| Services    | Database, Models, Interface, Helpers, Utils, Config |
| Interface   | Config                                        |
| Helpers     | Config                                        |
| Utils       | Ninguna                                       |
| Database    | Config                                        |
| Models      | Config                                        |
| Config      | Ninguna                                       |

## 7. Patrones de Diseño

### 7.1 Programación Funcional
- No se usan clases
- Las funciones son ciudadanos de primera clase
- Los diccionarios se usan para estructuras de datos
- Estilo de operación inmutable (las funciones retornan nuevas listas)

### 7.2 Separación de Responsabilidades
- Lógica de UI separada de lógica de negocio
- Lógica de negocio separada de acceso a datos
- Configuración centralizada

### 7.3 Inyección de Dependencias
- Las funciones reciben dependencias como parámetros
- Sin estado global (excepto constantes)
- Funciones puras donde sea posible

## 8. Estrategia de Manejo de Errores

1. **Capa de Validación**: La interfaz valida el formato de entrada del usuario
2. **Capa de Negocio**: Los servicios validan reglas de negocio
3. **Capa de Datos**: La base de datos maneja errores de persistencia
4. **Retroalimentación al Usuario**: Todos los errores se muestran a través de la capa de Interfaz

## 9. Puntos de Extensibilidad

La arquitectura soporta extensiones futuras:

1. **Nuevo Backend de Almacenamiento**: Reemplazar `json_store.py` con `sql_store.py`
2. **Nueva Interfaz**: Agregar capa `api/` junto a `interface/`
3. **Nuevas Validaciones**: Agregar validadores en `utils/validators.py`
4. **Nuevos Campos de Contacto**: Actualizar `models/contact.py` y agregar a config

## 10. Restricciones de Arquitectura

1. **Sin Clases**: Todo el código usa solo funciones y diccionarios
2. **Solo Biblioteca Estándar**: No se permiten dependencias externas
3. **Solo CLI**: Sin interfaz web o GUI
4. **Usuario Único**: Sin soporte de acceso concurrente
5. **En Memoria + JSON**: No se usa sistema de base de datos
