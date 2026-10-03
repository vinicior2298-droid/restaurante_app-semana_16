# Sistema de Gestión de Restaurante 

# Sistema de Gestión para Restaurante (`restaurante_app`)

Sistema de escritorio desarrollado en Python utilizando **Tkinter** para la interfaz gráfica y persistencia de datos mediante archivos **JSON**, estructurado bajo el patrón de arquitectura de separación de responsabilidades (MVC adaptado con Servicios y Modelos).

## 🚀 Características Principales Implementadas 

* **Autenticación y Navegación:** 
  * Sistema de inicio de sesión seguro con diferenciación de roles[cite: 10].
  * Navegación fluida entre las vistas de Gestión de Productos, Consulta de Usuarios y Gestión de Ventas.
* **Módulo Avanzado de Gestión de Usuarios:**
  * Registro, consulta, actualización y eliminación de usuarios directamente desde la interfaz gráfica.
  * Incorporación del atributo **rol** en el modelo `Usuario` para diferenciar entre **Administrador**, **Empleado** y **Cliente**.
  * Control de acceso exclusivo para usuarios con rol **Administrador** a la gestión administrativa de usuarios.
  * Visualización estructurada de los usuarios registrados en un componente `TreeView` (ID, nombre, usuario y rol).
* **Interactividad y Eventos (UI):**
  * Asociación del evento `<<TreeviewSelect>>` mediante `bind()` para cargar automáticamente los datos del usuario seleccionado hacia el formulario[cite: 10].
  * Uso de un `Combobox` interactivo para la selección dinámica del rol del usuario.
  * Implementación de atajos de teclado como `<Return>` para confirmar registros de forma rápida y `<Escape>` para limpiar el formulario y restablecer estados iniciales.
  * Botones dedicados (**Registrar**, **Actualizar**, **Eliminar** y **Limpiar**) enlazados mediante `command=`.
* **Persistencia y Lógica de Negocio:**
  * Toda la lógica de negocio, validaciones de stock y manipulación de archivos JSON se centraliza en la capa de servicios (`RestauranteServicio`).
  * Manejo seguro de la serialización de datos de ventas y productos en el directorio `/datos`.
  * Interfaz visual mejorada con soporte para recursos multimedia y logotipos institucionales en la carpeta `assets/`.

## 📂 Estructura del Proyecto

restaurante_app/
│
├── assets/              # Iconos, logotipos e imágenes del sistema
├── datos/               # Archivos JSON de persistencia (usuarios.json, productos.json, ventas.json)
├── modelos/             # Clases de entidades (producto.py, usuario.py, venta.py)
├── servicios/           # Lógica de negocio y manejo de archivos (archivo_servicio.py, restaurante_servicio.py)
├── ui/                  # Vistas de la interfaz gráfica (login_view.py, main_view.py)
└── main.py              # Punto de entrada principal de la aplicación