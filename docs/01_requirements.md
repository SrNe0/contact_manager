# Especificación de Requisitos

## 1. Requisitos Funcionales

### 1.1 Gestión de Contactos

**RF-001**: El sistema debe permitir a los usuarios crear un nuevo
contacto con los siguientes campos:

- Nombre (obligatorio)
- Número de teléfono (opcional)
- Dirección de correo electrónico (opcional)

**RF-002**: El sistema debe asignar automáticamente un ID numérico único
a cada contacto al momento de su creación.

**RF-003**: El sistema debe mostrar una lista de todos los contactos
almacenados con su ID, nombre, teléfono y correo electrónico.

**RF-004**: El sistema debe permitir a los usuarios buscar un contacto
por su ID único.

**RF-005**: El sistema debe permitir a los usuarios actualizar cualquier
campo de un contacto existente.

**RF-006**: El sistema debe permitir a los usuarios eliminar un contacto
después de una confirmación explícita.

**RF-007**: El sistema debe mostrar "No proporcionado" para los campos
opcionales que se dejen vacíos.

### 1.2 Persistencia de Datos

**RF-008**: El sistema debe cargar automáticamente los contactos desde
un archivo JSON al iniciar.

**RF-009**: El sistema debe guardar automáticamente los contactos en un
archivo JSON después de cualquier operación de creación, actualización
o eliminación.

**RF-010**: El sistema debe manejar archivos JSON faltantes o corruptos
de manera elegante, comenzando con una lista vacía de contactos y
mostrando un mensaje de error.

### 1.3 Interfaz de Usuario

**RF-011**: El sistema debe proporcionar una interfaz de menú en línea
de comandos con las siguientes opciones:

1. Agregar contacto
2. Ver todos los contactos
3. Buscar contacto
4. Actualizar contacto
5. Eliminar contacto
6. Salir

**RF-012**: El sistema debe limpiar la pantalla antes de mostrar el
menú.

**RF-013**: El sistema debe esperar la confirmación del usuario (tecla
Enter) antes de volver al menú principal después de cada operación.

**RF-014**: El sistema debe mostrar mensajes apropiados de éxito y
error para todas las operaciones.

### 1.4 Validación

**RF-015**: El sistema debe requerir que el campo de nombre del contacto
no esté vacío.

**RF-016**: El sistema debe validar que los números de teléfono
contengan solo dígitos (0-9).

**RF-017**: El sistema debe permitir entrada vacía para números de
teléfono durante la creación de contactos.

**RF-018**: El sistema debe permitir entrada vacía para todos los campos
durante la actualización de contactos, tratando la entrada vacía como
"mantener valor actual".

**RF-019**: El sistema debe validar que la entrada del usuario para el
ID del contacto sea un entero válido.

**RF-020**: El sistema debe validar que las selecciones del menú sean
enteros válidos.

## 2. Requisitos No Funcionales

### 2.1 Rendimiento

**RNF-001**: El sistema debe cargar y mostrar el menú en menos de 1
segundo en hardware estándar.

**RNF-002**: El sistema debe guardar contactos en el archivo JSON en
menos de 100 milisegundos para conjuntos de datos de hasta 10,000
contactos.

### 2.2 Usabilidad

**RNF-003**: El sistema debe mostrar mensajes de error claros que
expliquen qué salió mal y cómo corregirlo.

**RNF-004**: El sistema debe usar formato consistente para todas las
visualizaciones de menú e información de contactos.

**RNF-005**: El sistema debe proporcionar indicaciones en línea que
indiquen el formato de entrada esperado (ej., "solo dígitos").

### 2.3 Mantenibilidad

**RNF-006**: El sistema debe seguir los estándares de codificación PEP 8
con indentación de 4 espacios y longitud máxima de línea de 88
caracteres.

**RNF-007**: El sistema debe usar una arquitectura en capas que separe
las responsabilidades (UI, lógica de negocio, acceso a datos).

**RNF-008**: El sistema debe evitar la programación orientada a objetos
(sin clases), usando solo funciones y estructuras de datos.

**RNF-009**: Todas las funciones públicas deben tener docstrings que
documenten el propósito, argumentos y valores de retorno.

**RNF-010**: Toda la documentación técnica y comentarios de código deben
estar escritos en inglés.

### 2.4 Confiabilidad

**RNF-011**: El sistema no debe perder datos si el archivo JSON está
corrupto; debe comenzar con una lista vacía en su lugar.

**RNF-012**: El sistema debe generar IDs de contacto únicos incluso
después de que se eliminen contactos.

### 2.5 Portabilidad

**RNF-013**: El sistema debe ejecutarse en cualquier plataforma con
Python 3.7 o superior.

**RNF-014**: El sistema debe usar solo módulos de la biblioteca estándar
de Python (sin dependencias externas).

**RNF-015**: El sistema debe usar códigos de escape ANSI para limpiar la
pantalla, compatible con la mayoría de los terminales modernos.

## 3. Supuestos

**S-001**: Los usuarios tienen conocimientos básicos de interfaz de
línea de comandos.

**S-002**: El terminal soporta códigos de escape ANSI para limpiar la
pantalla.

**S-003**: El volumen de datos de contactos no excederá los 100,000
registros (limitación del tamaño del archivo JSON).

**S-004**: Las direcciones de correo electrónico no requieren validación
de formato para esta versión.

**S-005**: Los números de teléfono se almacenan como cadenas para
preservar ceros a la izquierda y soportar formatos internacionales.

**S-006**: Múltiples usuarios no accederán al mismo archivo
contacts.json simultáneamente.

## 4. Restricciones

**R-001**: El sistema no debe usar programación orientada a objetos
(sin clases).

**R-002**: El sistema debe usar JSON para almacenamiento de datos
(sin base de datos).

**R-003**: El sistema debe implementarse como una interfaz de línea de
comandos (sin GUI).

**R-004**: El sistema debe usar solo la biblioteca estándar de Python
(sin paquetes externos).

**R-005**: El sistema debe mantener compatibilidad con archivos
contacts.json existentes.

## 5. Fuera de Alcance

Las siguientes funcionalidades están explícitamente excluidas de la
versión actual:

- Funcionalidad de importación/exportación (CSV, vCard)
- Grupos o categorías de contactos
- Búsqueda por nombre o correo electrónico
- Detección de duplicados
- Cifrado de datos
- Soporte multiusuario
- Historial/auditoría de contactos
- Validación de formato de correo electrónico
- Funcionalidad de deshacer/rehacer
