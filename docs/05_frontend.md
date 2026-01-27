# Documentación de Frontend

## 1. Resumen

El frontend del Contact Manager es una **interfaz de línea de comandos (CLI)** que proporciona una experiencia interactiva basada en menús. La capa de interfaz maneja toda la interacción del usuario, validación de entrada y formato de salida.

## 2. Arquitectura de Interfaz

**Ubicación**: `app/interface/menu.py`

**Tipo**: Interfaz de terminal basada en texto

**Estilo**: Basado en menú con opciones numeradas

**Modelo de Interacción**: Solicitud-respuesta síncrona

## 3. Menú Principal

### 3.1 Diseño del Menú

Ver: [wireframes/main_menu.txt](wireframes/main_menu.txt)

```
==================================================
                 CONTACT MANAGER
==================================================
1. Agregar contacto
2. Ver todos los contactos
3. Buscar contacto
4. Actualizar contacto
5. Eliminar contacto
6. Salir
==================================================

Seleccione opción (1-6): _
```

**Especificaciones del Menú**:
- Ancho: 50 caracteres (configurable vía MENU_WIDTH)
- Borde: Caracteres `=`
- Título: Centrado usando método `.center()`
- Opciones: Numeradas 1-6
- Mensaje: Instrucción clara de selección

### 3.2 Comportamiento del Menú

**Al Entrar**:
1. La pantalla se limpia usando códigos de escape ANSI
2. El menú se muestra
3. El cursor espera en el mensaje de opción

**Al Seleccionar**:
1. El usuario ingresa un número (1-6)
2. Si es 6: salir de la aplicación
3. Si es inválida: mostrar error, esperar Enter, volver a mostrar menú
4. Si es válida: ejecutar acción correspondiente

**Al Completar Acción**:
1. Mostrar resultados de la operación
2. Esperar que el usuario presione Enter
3. Volver al menú (limpiado y redibujado)

## 4. Estados de Pantalla

### 4.1 Pantalla de Bienvenida

**Mostrada**: Al iniciar la aplicación (antes del primer menú)

```
¡Bienvenido a Contact Manager!

[Aparece el menú principal]
```

### 4.2 Pantalla de Agregar Contacto

```
--- AGREGAR NUEVO CONTACTO ---
Nombre: _
```

**Flujo del Usuario**:
1. Ingresar nombre (requerido)
2. Ingresar teléfono (opcional, solo dígitos)
3. Ingresar email (opcional)
4. Ver mensaje de éxito
5. Presionar Enter para volver al menú

**Mensajes de Validación**:
- Nombre vacío: "Error: El nombre no puede estar vacío." → volver al menú
- Teléfono inválido: "Error: El teléfono debe contener solo dígitos (0-9)." → volver a solicitar

**Mensaje de Éxito**:
```
¡Contacto 'John Doe' agregado exitosamente!

Presione Enter para continuar...
```

### 4.3 Pantalla de Ver Todos los Contactos

```
--- TODOS LOS CONTACTOS ---

[1] John Doe
    Teléfono: 1234567890
    Email: john@example.com

[2] Jane Smith
    Teléfono: No proporcionado
    Email: jane@example.com

Presione Enter para continuar...
```

**Estado Vacío**:
```
--- TODOS LOS CONTACTOS ---
No se encontraron contactos.

Presione Enter para continuar...
```

### 4.4 Pantalla de Buscar Contacto

```
--- BUSCAR CONTACTO ---
Ingrese ID del contacto: _
```

**Caso Encontrado**:
```
ID: 1
Nombre: John Doe
Teléfono: 1234567890
Email: john@example.com
--------------------------------------------------

Presione Enter para continuar...
```

**Caso No Encontrado**:
```
No se encontró contacto con ID 5.

Presione Enter para continuar...
```

**Caso Lista Vacía**:
```
--- BUSCAR CONTACTO ---
No hay contactos disponibles.

Presione Enter para continuar...
```

### 4.5 Pantalla de Actualizar Contacto

```
--- ACTUALIZAR CONTACTO ---
Ingrese ID del contacto: _
```

**Después de Ingresar ID**:
```
Información actual:

ID: 1
Nombre: John Doe
Teléfono: 1234567890
Email: john@example.com
--------------------------------------------------

Ingrese nuevos valores (presione Enter para mantener actual):
Nombre: _
```

**Continuación**:
```
Nombre: John Smith
Teléfono (solo dígitos): _
```

```
Teléfono (solo dígitos): 9876543210
Email: _
```

```
Email: johnsmith@example.com

¡Contacto actualizado exitosamente!

Presione Enter para continuar...
```

**Manteniendo Valores Actuales**:
```
Nombre: [Enter]                ← mantiene actual
Teléfono (solo dígitos): [Enter] ← mantiene actual
Email: [Enter]               ← mantiene actual

¡Contacto actualizado exitosamente!
```

### 4.6 Pantalla de Eliminar Contacto

```
--- ELIMINAR CONTACTO ---
Ingrese ID del contacto: _
```

**Después de Ingresar ID**:
```
Contacto a eliminar:

ID: 1
Nombre: John Doe
Teléfono: 1234567890
Email: john@example.com
--------------------------------------------------

¿Está seguro? (yes/no): _
```

**Eliminación Confirmada**:
```
Contacto 'John Doe' eliminado.

Presione Enter para continuar...
```

**Eliminación Cancelada**:
```
Eliminación cancelada.

Presione Enter para continuar...
```

### 4.7 Pantalla de Salida

```
¡Gracias por usar Contact Manager!
```

**Comportamiento**: La aplicación termina después de este mensaje

### 4.8 Pantalla de Opción Inválida

```
Opción inválida. Por favor seleccione 1-6.

Presione Enter para continuar...
```

**Comportamiento**: Vuelve al menú principal después de Enter

## 5. Funciones de Entrada

### 5.1 Entrada de Cadena

**Función**: `prompt_string(message)`

**Propósito**: Entrada genérica de cadena con recorte de espacios

**Uso**:
```python
name = prompt_string("Nombre: ")
email = prompt_string("Email (opcional): ")
```

**Comportamiento**: Retorna cadena recortada (puede estar vacía)

### 5.2 Entrada de Entero

**Función**: `prompt_int(message)`

**Propósito**: Entrada de entero validada con bucle de reintento

**Uso**:
```python
contact_id = prompt_int("Ingrese ID del contacto: ")
```

**Comportamiento**:
- Bucle hasta que se ingrese un entero válido
- Muestra error en entrada inválida: "Error: Por favor ingrese un entero válido."

### 5.3 Entrada de Confirmación

**Función**: `prompt_confirmation(message)`

**Propósito**: Confirmación sí/no

**Uso**:
```python
confirmation = prompt_confirmation("¿Está seguro? (yes/no): ")
if confirmation in CONFIRM_YES_VALUES:
    # proceder
```

**Comportamiento**: Retorna cadena en minúsculas y recortada

**Valores Aceptados**: "yes", "y" (insensible a mayúsculas)

### 5.4 Entrada de Teléfono

**Función**: `prompt_phone_digits(message, allow_empty)`

**Ubicación**: `app/utils/validators.py` (utilidad de validación)

**Propósito**: Validación de número de teléfono

**Uso**:
```python
phone = prompt_phone_digits("Teléfono (solo dígitos, opcional): ", allow_empty=True)
```

**Comportamiento**:
- Si allow_empty=True y entrada es vacía: retorna ""
- Si entrada contiene solo dígitos: retorna entrada
- De lo contrario: muestra error y vuelve a solicitar

## 6. Funciones de Salida

### 6.1 Imprimir Mensaje

**Función**: `print_message(message)`

**Propósito**: Mostrar información al usuario

**Uso**:
```python
print_message("¡Contacto agregado exitosamente!")
print_message("No se encontraron contactos.")
```

### 6.2 Imprimir Error

**Función**: `print_error(message)`

**Propósito**: Mostrar mensajes de error

**Uso**:
```python
print_error("El nombre no puede estar vacío.")
```

**Formato**: `Error: {mensaje}`

### 6.3 Esperar Enter

**Función**: `wait_for_enter()`

**Propósito**: Pausar hasta que el usuario presione Enter

**Uso**:
```python
wait_for_enter()  # Muestra: "Presione Enter para continuar..."
```

## 7. Gestión de Pantalla

### 7.1 Limpiar Pantalla

**Función**: `clear_screen()`

**Ubicación**: `app/utils/console.py`

**Propósito**: Limpiar la visualización del terminal

**Implementación**: Códigos de escape ANSI `\033[2J\033[H`

**Compatibilidad**: Funciona en la mayoría de terminales modernos (Linux, macOS, Windows 10+)

**Uso**:
```python
clear_screen()  # Limpia pantalla y mueve cursor a arriba-izquierda
```

### 7.2 Visualización de Menú

**Función**: `show_menu()`

**Propósito**: Mostrar menú principal

**Diseño**:
- Borde superior (50 caracteres `=`)
- Título centrado
- Borde medio
- 6 opciones numeradas
- Borde inferior

## 8. Patrones de Interacción del Usuario

### 8.1 Flujo de Operación Estándar

```
┌─────────────────────┐
│  Limpiar Pantalla   │
├─────────────────────┤
│  Mostrar Menú       │
├─────────────────────┤
│  Obtener Elección   │
├─────────────────────┤
│  Ejecutar Acción    │
├─────────────────────┤
│  Mostrar Resultados │
├─────────────────────┤
│  Esperar Enter      │
└─────────────────────┘
        │
        └──> Volver al inicio
```

### 8.2 Flujo de Validación

```
┌──────────────────────┐
│  Solicitar Entrada   │
├──────────────────────┤
│  Validar Entrada     │
└──────┬───────────────┘
       │
       ├─ Válida ──> Retornar valor
       │
       └─ Inválida ──> Mostrar error
                   └──> Volver al inicio
```

### 8.3 Flujo de Confirmación

```
┌──────────────────────┐
│  Mostrar Elemento    │
├──────────────────────┤
│  Pedir Confirmación  │
└──────┬───────────────┘
       │
       ├─ Sí ──> Proceder con acción
       │
       └─ No ──> Cancelar y retornar
```

## 9. Mensajes de Error

| Escenario | Mensaje |
|-----------|---------|
| Opción de menú inválida | "Opción inválida. Por favor seleccione 1-6." |
| Entero inválido | "Error: Por favor ingrese un entero válido." |
| Teléfono inválido | "Error: El teléfono debe contener solo dígitos (0-9)." |
| Nombre vacío | "Error: El nombre no puede estar vacío." |
| Contacto no encontrado | "No se encontró contacto con ID {id}." |
| Sin contactos (buscar) | "No hay contactos disponibles." |
| Sin contactos (ver) | "No se encontraron contactos." |

## 10. Mensajes de Éxito

| Operación | Mensaje |
|-----------|---------|
| Agregar contacto | "¡Contacto '{name}' agregado exitosamente!" |
| Actualizar contacto | "¡Contacto actualizado exitosamente!" |
| Eliminar contacto | "Contacto '{name}' eliminado." |
| Cancelar eliminación | "Eliminación cancelada." |

## 11. Helpers de Formato

**Ubicación**: `app/helpers/formatters.py`

### 11.1 Formato de Contacto Individual

**Función**: `format_contact(contact)`

**Salida**:
```
ID: 1
Nombre: John Doe
Teléfono: 1234567890
Email: john@example.com
--------------------------------------------------
```

### 11.2 Formato de Lista de Contactos

**Función**: `format_contact_list(contacts)`

**Salida**:
```
[1] John Doe
    Teléfono: 1234567890
    Email: john@example.com

[2] Jane Smith
    Teléfono: No proporcionado
    Email: jane@example.com
```

## 12. Consideraciones de Accesibilidad

### 12.1 Compatibilidad con Lectores de Pantalla

- Todos los mensajes son texto claro
- Sin dependencia solo en formato visual
- Los mensajes de estado son explícitos

### 12.2 Navegación Solo con Teclado

- Todas las interacciones vía teclado
- No se requiere mouse
- Tecla Enter para confirmación

### 12.3 Instrucciones Claras

- Cada mensaje explica la entrada esperada
- Los errores de validación explican qué salió mal
- Los campos opcionales marcados como "(opcional)"

## 13. Requisitos del Terminal

**Requisitos Mínimos**:
- Soporte de códigos de escape ANSI (limpieza de pantalla)
- Codificación UTF-8 (caracteres internacionales)
- Flujos estándar de entrada/salida

**Entornos Probados**:
- Terminales Linux (bash, zsh)
- Terminal de macOS
- Windows Terminal / PowerShell 7+
- Símbolo del sistema de Windows (Windows 10+)

## 14. Wireframes

Ver: [wireframes/main_menu.txt](wireframes/main_menu.txt) para wireframes ASCII

## 15. Mejoras Futuras de UI (Fuera de Alcance)

- Mensajes codificados por color (éxito=verde, error=rojo)
- Indicadores de progreso para carga
- Visualización de lista de contactos basada en tabla
- Paginación para listas grandes de contactos
- Búsqueda por nombre/email
- Opciones de ordenamiento (por nombre, por ID)
- Exportar a CSV/archivo de texto
- Atajos de teclado (Ctrl+C para cancelar)
