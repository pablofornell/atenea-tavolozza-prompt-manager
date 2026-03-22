# SPEC.md - Travolozza

## 1. Visión General
**Travolozza** es una aplicación de escritorio ligera diseñada para facilitar la ingeniería de prompts (Prompt Engineering). Permite a los usuarios construir prompts complejos de manera modular, separando las ideas en distintos bloques de texto e integrando imágenes de contexto. El objetivo final es unificar todo el contenido con un solo clic para pegarlo directamente en el chatbot de IA de su preferencia (como Gemini, ChatGPT, Claude, etc.).

## 2. Interfaz de Usuario (UI)
Basado en el boceto, la interfaz se divide en tres áreas principales de arriba hacia abajo:

* **Zona de Contexto Visual (Cabecera):**
    * Una fila horizontal superior dedicada a las imágenes.
    * Muestra miniaturas de las imágenes cargadas.
    * Incluye un botón cuadrado con un ícono de **`+`** para abrir el explorador de archivos y añadir nuevas imágenes al contexto.
* **Zona de Construcción de Prompt (Centro):**
    * Una lista vertical dinámica de campos de texto (`<textarea>`).
    * Cada campo representa un "bloque" o "módulo" del prompt (ej. Instrucción principal, Formato deseado, Ejemplos, Tono).
    * Debajo de los bloques de texto existentes, hay un botón circular con un ícono de **`+`** para añadir un nuevo bloque de texto vacío a la lista.
* **Zona de Acción (Pie de página):**
    * Un botón prominente etiquetado como **`Copy`** en la esquina inferior derecha.

## 3. Requisitos Funcionales

### 3.1. Gestión de Texto (Bloques modulares)
* **Creación:** El usuario debe poder añadir múltiples bloques de texto independientes a través de la UI.
* **Edición:** Cada bloque debe ser editable en tiempo real.
* **Eliminación:** Cada bloque debe contar con un control para ser eliminado de la lista.

### 3.2. Gestión de Imágenes
* **Importación:** El usuario puede añadir imágenes haciendo clic en el botón `+` de la cabecera. La UI debe pasar la ruta de la imagen a Python para su procesamiento.
* **Visualización:** Las imágenes deben mostrarse como miniaturas en la barra superior.
* **Eliminación:** El usuario debe poder remover una imagen de la lista.

### 3.3. Exportación (Procesamiento en Python)
* **Recolección de Datos:** Al hacer clic en "Copy", el frontend (JS) recolecta el texto de todos los bloques y las rutas de las imágenes, enviándolos a la función expuesta de Python.
* **Concatenación:** Python une el texto de todos los bloques en un solo string, separados por un salto de línea doble (`\n\n`).
* **Copia al Portapapeles Multiplataforma:** * El script de Python detectará el sistema operativo (`os.name` o `sys.platform`).
    * **Windows:** Utilizará librerías como `win32clipboard` para inyectar formatos MIME múltiples (texto e imagen) en el portapapeles de Windows.
    * **macOS:** Utilizará `AppKit` (PyObjC) o comandos de sistema como `pbcopy` para gestionar el portapapeles de Mac.
    * **Linux:** Utilizará herramientas de sistema como `xclip` o `xsel` para gestionar las selecciones del portapapeles.
    * *Nota técnica:* Copiar texto e imágenes simultáneamente requiere escribir formatos MIME específicos (`text/plain` y `image/png` o `text/uri-list`) para que los navegadores modernos los interpreten correctamente al pegar en un input de un chatbot.

## 4. Flujo de Usuario (User Journey)
1.  El usuario abre **Travolozza**.
2.  (Opcional) Hace clic en el botón `+` superior para añadir fotos de referencia.
3.  Escribe el contexto inicial en el primer bloque de texto.
4.  Hace clic en el botón circular `+` para añadir un segundo bloque y escribe más instrucciones.
5.  Hace clic en **`Copy`**. La UI envía la orden a Python.
6.  Python procesa y carga el portapapeles del sistema operativo correspondiente.
7.  El usuario va a su navegador y pega (`Ctrl+V` / `Cmd+V`) el resultado en su IA favorita.

## 5. Pila Tecnológica (Tech Stack)
* **Backend y Lógica de Sistema:** `Python 3.x`.
* **Framework de Escritorio:** `Eel` o `PyWebView` (para levantar la ventana de UI nativa y comunicar JS con Python sin necesidad de un servidor local complejo).
* **Gestión de Portapapeles:** Librerías específicas del OS integradas en el script de Python (`pywin32` para Windows, `pyobjc` para Mac, llamadas a `subprocess` para Linux, o probar abstracciones como `PyQt6` solo para el módulo del portapapeles si la lógica nativa se complica).
* **Frontend:** `HTML5` semántico, `CSS3` (Grid/Flexbox para el diseño) y `Vanilla JavaScript` (solo para la interactividad de la UI y la comunicación con Python).