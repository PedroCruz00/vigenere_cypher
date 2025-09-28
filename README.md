# Cifrado Vigenère

Una implementación del cifrado Vigenère con soporte para cifrado, descifrado y un módulo básico de criptoanálisis (estimación de longitud de clave y recuperación de clave) mediante el método Kasiski. Incluye una interfaz gráfica para una experiencia interactiva.

## Descripción

El cifrado Vigenère es un método de cifrado polialfabético que utiliza una clave para desplazar letras del texto de acuerdo con una tabla de sustitución. Esta implementación permite:

- Cifrar y descifrar texto.
- Analizar texto cifrado para estimar la clave usando repeticiones de n-gramas.
- Normalización de texto en modos "strict" (solo letras A-Z) y "lax" (conserva puntuación y espacios).
- Validación de entradas y manejo de errores.

## Instrucciones de Uso

1. **Instalación**:

   - Asegúrate de tener Python 3.x instalado. Verifica con `python3 --version`.
   - Instala las dependencias necesarias:
     - tkinter (generalmente incluido, pero si no está, usa el gestor de paquetes de tu sistema):
       - En Ubuntu/Debian: `sudo apt-get install python3-tk`
       - En Fedora: `sudo dnf install python3-tkinter`
       - En macOS (con Homebrew): `brew install python-tk`
       - En Windows: tkinter viene con la instalación estándar de Python.
   - No se requieren paquetes adicionales vía pip para este proyecto.

2. **Ejecución**: Ejecuta `vigenere_gui.py` con Python 3.

   - Comando: `python3 vigenere_gui.py`

3. **Interfaz Gráfica**:

   - **Modo**: Selecciona "encrypt", "decrypt" o "analyze".
   - **Texto**: Ingresa el texto o usa "Cargar archivo" para cargar desde un `.txt`.
   - **Clave**: Ingresa la clave (requerida para cifrar/descifrar).
   - **Normalización**: Elige "strict" o "lax".
   - **Alfabeto**: Opcional, por defecto es A-Z.
   - **Procesar**: Haz clic en "Procesar" para obtener el resultado.
   - **Guardar**: Usa "Guardar resultado" para salvar el output en un `.txt`.

4. **Modos**:

   - **Encrypt**: Cifra el texto con la clave proporcionada.
   - **Decrypt**: Descifra el texto con la clave proporcionada.
   - **Analyze**: Estima la clave y descifra el texto automáticamente.

5. **Errores**: Mensajes de error aparecerán si la clave es vacía o el texto es inválido.

## Ejemplos de Uso

- Texto: "HELLO", Clave: "KEY", Modo: "encrypt", Normalización: "strict" → Resultado: "RIJVS".
- Texto: "RIJVS", Clave: "KEY", Modo: "decrypt", Normalización: "strict" → Resultado: "HELLO".
- Texto largo cifrado, Modo: "analyze" → Estima clave y muestra texto descifrado.

## Límites Conocidos

- El análisis Kasiski requiere textos largos (>50 caracteres) para ser efectivo.
- La estimación de clave puede fallar con claves muy cortas o sin repeticiones claras.
- No soporta alfabeto con caracteres no latinos (e.g., ñ) a menos que se especifique manualmente.

## Requisitos

- Python 3.x
- tkinter (incluido por defecto en la mayoría de instalaciones de Python)

## Licencia

License - Copyright (c) 2025

## Autoría

Desarrollado por Estudiantes de Electiva IV (Seguridad Computacional) de la UPTC sin asistencia automática el 27 de septiembre de 2025.
