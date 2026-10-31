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

**RF-004**: El sistema debe permitir a los usuarios buscar contactos por
ID exacto o por coincidencia parcial en nombre, teléfono o correo
electrónico, sin distinguir mayúsculas de minúsculas.

**RF-005**: El sistema debe permitir a los usuarios actualizar cualquier
campo de un contacto existente y vaciar el teléfono o el correo
electrónico.

**RF-006**: El sistema debe permitir a los usuarios eliminar un contacto
después de una confirmación explícita.

**RF-007**: El sistema debe mostrar "Not provided" para los campos
opcionales que se dejen vacíos.

**RF-021**: El sistema debe advertir si el teléfono o el correo
electrónico ya pertenecen a otro contacto, y guardar solo si el usuario
lo confirma.

**RF-022**: El sistema debe permitir exportar todos los contactos a un
archivo CSV compatible con hojas de cálculo.

### 1.2 Persistencia de Datos

**RF-008**: El sistema debe cargar automáticamente los contactos desde
un archivo JSON al iniciar.

**RF-009**: El sistema debe guardar automáticamente los contactos en un
archivo JSON después de cualquier operación de creación, actualización
o eliminación.

**RF-010**: El sistema debe comenzar con una lista vacía si el archivo
JSON no existe. Si el archivo está dañado, debe conservarlo como respaldo
y mostrar una advertencia que el usuario pueda leer antes de ver el menú.

**RF-023**: El sistema debe recuperar los registros válidos de un archivo
parcialmente dañado, completar los campos opcionales faltantes y asignar
un ID nuevo a los registros con ID ausente, inválido o duplicado.

**RF-024**: Si el archivo existe pero no se puede leer, el sistema debe
mostrar el error y cerrarse sin modificar el archivo.

**RF-025**: Si un guardado falla, el sistema debe mostrar el error,
descartar el cambio y no informar éxito.

### 1.3 Interfaz de Usuario

**RF-011**: El sistema debe proporcionar una interfaz de menú en línea
de comandos con las siguientes opciones:

1. Agregar contacto
2. Ver todos los contactos
3. Buscar contactos
4. Actualizar contacto
5. Eliminar contacto
6. Exportar a CSV
7. Salir

**RF-012**: El sistema debe limpiar la pantalla antes de mostrar el
menú.

**RF-013**: El sistema debe esperar la confirmación del usuario (tecla
Enter) antes de volver al menú principal después de cada operación.

**RF-014**: El sistema debe mostrar mensajes apropiados de éxito y
error para todas las operaciones.

**RF-026**: El sistema debe cerrarse sin mostrar un traceback cuando el
usuario presione Ctrl+C o termine la entrada estándar.

### 1.4 Validación

**RF-015**: El sistema debe requerir que el campo de nombre del contacto
no esté vacío.

**RF-016**: El sistema debe validar que los números de teléfono
contengan solo dígitos ASCII (0-9).

**RF-017**: El sistema debe permitir entrada vacía para teléfono y correo
electrónico durante la creación de contactos.

**RF-018**: El sistema debe permitir entrada vacía para todos los campos
durante la actualización de contactos, tratándola como "mantener valor
actual". El valor `-` vacía el teléfono o el correo electrónico.

**RF-019**: El sistema debe validar que el ID ingresado sea un entero
positivo escrito solo con dígitos ASCII.

**RF-020**: El sistema debe rechazar las selecciones de menú fuera de
las opciones disponibles.

**RF-027**: El sistema debe validar que los correos electrónicos
ingresados tengan la forma `nombre@dominio.tld`.

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
con indentación de 4 espacios, longitud máxima de línea de 88 caracteres
y anotaciones de tipos.

**RNF-007**: El sistema debe usar una arquitectura en capas que separe
las responsabilidades (UI, lógica de negocio, acceso a datos).

**RNF-008**: El sistema debe evitar la programación orientada a objetos
(sin clases), usando solo funciones y estructuras de datos. Las pruebas
pueden usar `unittest.TestCase`.

**RNF-009**: Todas las funciones públicas deben tener docstrings estilo
Google que documenten el propósito, argumentos, valores de retorno y
excepciones.

**RNF-010**: El código, los comentarios y los mensajes de la aplicación
deben estar en inglés. La documentación de `docs/` se mantiene en español.

**RNF-016**: La lógica de negocio, los validadores y la persistencia deben
contar con pruebas unitarias automatizadas en `tests/`.

### 2.4 Confiabilidad

**RNF-011**: El sistema no debe perder datos si el archivo JSON está
dañado: debe conservar una copia antes de continuar.

**RNF-012**: El sistema debe generar IDs distintos a los de todos los
contactos existentes.

**RNF-017**: Los guardados deben ser atómicos: un fallo durante la
escritura debe dejar intacto el archivo anterior.

### 2.5 Portabilidad

**RNF-013**: El sistema debe ejecutarse en cualquier plataforma con
Python 3.9 o superior.

**RNF-014**: El sistema debe usar solo módulos de la biblioteca estándar
de Python para ejecutarse y probarse (sin dependencias externas).

**RNF-015**: El sistema debe usar códigos de escape ANSI para limpiar la
pantalla, compatible con la mayoría de los terminales modernos.

**RNF-018**: El sistema debe encontrar `contacts.json` en la raíz del
proyecto, sin importar desde qué directorio se ejecute.

## 3. Supuestos

**S-001**: Los usuarios tienen conocimientos básicos de interfaz de
línea de comandos.

**S-002**: El terminal soporta códigos de escape ANSI para limpiar la
pantalla.

**S-003**: El volumen de datos de contactos no excederá los 100,000
registros (limitación del tamaño del archivo JSON).

**S-004**: La validación de correo electrónico revisa solo el formato;
no comprueba que la dirección exista.

**S-005**: Los números de teléfono se almacenan como cadenas para
preservar ceros a la izquierda.

**S-006**: Múltiples usuarios no accederán al mismo archivo
contacts.json simultáneamente.

## 4. Restricciones

**R-001**: El código de la aplicación no debe usar programación orientada
a objetos (sin clases).

**R-002**: El sistema debe usar JSON para almacenamiento de datos
(sin base de datos).

**R-003**: El sistema debe implementarse como una interfaz de línea de
comandos (sin GUI).

**R-004**: La aplicación y sus pruebas deben usar solo la biblioteca
estándar de Python.

**R-005**: El sistema debe mantener compatibilidad con archivos
contacts.json existentes.

**R-006**: Los datos personales (`contacts.json`, sus respaldos y las
exportaciones CSV) no deben versionarse en git.

## 5. Fuera de Alcance

Las siguientes funcionalidades están explícitamente excluidas de la
versión actual:

- Importación de archivos (CSV, vCard) y exportación a vCard
- Grupos o categorías de contactos
- Cifrado de datos
- Soporte multiusuario
- Historial/auditoría de contactos
- Funcionalidad de deshacer/rehacer
