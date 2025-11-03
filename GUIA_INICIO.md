# 📖 GUÍA DE INICIO PASO A PASO

Esta guía te llevará desde cero hasta tener tu aplicación funcionando.

## ✅ REQUISITOS PREVIOS

Antes de empezar, asegúrate de tener instalado:

1. **Python 3.8 o superior**
   - Descarga: https://www.python.org/downloads/
   - Durante la instalación, marca "Add Python to PATH"
   - Verifica instalación: abre CMD y ejecuta `python --version`

2. **Visual Studio Code** (recomendado)
   - Descarga: https://code.visualstudio.com/
   - Instala la extensión de Python

3. **Git** (opcional, pero recomendado)
   - Descarga: https://git-scm.com/downloads

## 🚀 PASO A PASO COMPLETO

### PASO 1: Preparar el Proyecto

1. **Descomprime** la carpeta del proyecto en una ubicación de tu preferencia
   - Ejemplo: `C:\Users\TuUsuario\Desktop\sistema-participacion`

2. **Abre VS Code**

3. **Abre la carpeta del proyecto**
   - En VS Code: `File → Open Folder`
   - Selecciona la carpeta `sistema-participacion`

### PASO 2: Crear Entorno Virtual

1. **Abre la terminal integrada en VS Code**
   - Atajo: `Ctrl + ñ` o `` Ctrl + ` ``
   - O desde el menú: `Terminal → New Terminal`

2. **Crea el entorno virtual**
   ```bash
   python -m venv venv
   ```
   
   Espera a que termine (puede tomar 1-2 minutos)
   
   ✅ Verás que se creó una carpeta llamada `venv`

### PASO 3: Activar Entorno Virtual

#### Si usas CMD (Command Prompt):
```bash
venv\Scripts\activate
```

#### Si usas PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

**¿Error de permisos en PowerShell?**
Ejecuta esto primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Luego intenta activar de nuevo.

✅ **Sabrás que funcionó** cuando veas `(venv)` al inicio de la línea en tu terminal:
```
(venv) C:\Users\TuUsuario\Desktop\sistema-participacion>
```

### PASO 4: Instalar Dependencias

Con el entorno virtual **ACTIVADO**, ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias. Puede tomar 2-5 minutos.

Verás algo como:
```
Installing collected packages: customtkinter, pillow, pyodbc...
Successfully installed customtkinter-5.2.2 pillow-10.3.0 ...
```

### PASO 5: Configurar Variables de Entorno

1. En la carpeta del proyecto, ya existe un archivo `.env`

2. **Si NO vas a usar SQL Server** (modo offline únicamente):
   - No necesitas cambiar nada, el archivo `.env` ya está configurado
   - Por defecto `AUTO_SYNC=False` (sin sincronización)

3. **Si SÍ quieres usar SQL Server** (sincronización online):
   - Abre el archivo `.env` en VS Code
   - Edita las credenciales de SQL Server:
   ```env
   SQL_SERVER_HOST=localhost
   SQL_SERVER_DATABASE=sistema_participacion
   SQL_SERVER_USER=tu_usuario
   SQL_SERVER_PASSWORD=tu_contraseña
   AUTO_SYNC=True
   ```

### PASO 6: Ejecutar la Aplicación

#### Opción A: Desde VS Code
Con el entorno virtual activado:
```bash
python src/main.py
```

#### Opción B: Doble clic en `run.bat` (Windows)
Solo funciona si ya hiciste los pasos anteriores.

### PASO 7: Iniciar Sesión

La aplicación abrirá una ventana de login.

**Credenciales por defecto:**
- Email: `admin@sistema.com`
- Contraseña: `admin123`

¡Listo! Ya estás dentro del sistema. 🎉

## 🎯 PRÓXIMOS PASOS

Ahora que tienes el sistema funcionando:

1. **Explora la interfaz**
   - Navega por las secciones del menú lateral
   - Dashboard, Alumnos, Participación, Clases, etc.

2. **Crea tu primer usuario**
   - En la ventana de login, haz clic en "Registrarse"
   - Crea una cuenta con tu email

3. **Empieza a desarrollar**
   - Los archivos principales están en `src/`
   - La interfaz está en `src/ui/`
   - Los modelos de BD en `src/database/models.py`

## ❓ PROBLEMAS COMUNES

### 1. "python: command not found"
**Solución:** Python no está instalado o no está en el PATH
- Reinstala Python marcando "Add Python to PATH"
- O descárgalo de: https://www.python.org/downloads/

### 2. "No module named 'customtkinter'"
**Solución:** Las dependencias no se instalaron correctamente
```bash
# Activa el entorno virtual primero
venv\Scripts\activate

# Reinstala las dependencias
pip install -r requirements.txt --force-reinstall
```

### 3. El entorno virtual no se activa
**Solución:** 
- Asegúrate de estar en la carpeta del proyecto
- En PowerShell, ejecuta:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 4. Error con pyodbc (SQL Server)
**Solución:** 
- Si no vas a usar SQL Server, pon `AUTO_SYNC=False` en `.env`
- Si sí quieres usarlo, instala ODBC Driver 17:
  https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### 5. La ventana no se abre
**Solución:**
- Revisa el archivo `logs/app.log` para ver el error
- Verifica que Python sea 3.8 o superior: `python --version`

### 6. "ModuleNotFoundError: No module named 'src'"
**Solución:** Estás ejecutando desde la carpeta incorrecta
```bash
# Asegúrate de estar en la raíz del proyecto
cd C:\ruta\a\sistema-participacion

# Luego ejecuta
python src/main.py
```

## 📞 NECESITAS MÁS AYUDA?

1. **Revisa los logs:**
   - Archivo: `logs/app.log`
   - Aquí se registra todo lo que pasa en la app

2. **Verifica la estructura:**
   ```
   sistema-participacion/
   ├── venv/                 ← Debe existir después del paso 2
   ├── src/
   │   ├── main.py          ← Punto de entrada
   │   └── ...
   ├── requirements.txt
   ├── .env                 ← Debe existir
   └── README.md
   ```

3. **Prueba la instalación básica:**
   ```bash
   # Activa el entorno
   venv\Scripts\activate
   
   # Verifica las dependencias
   pip list
   
   # Debe aparecer customtkinter, sqlalchemy, etc.
   ```

## 🔄 REINICIAR DESDE CERO

Si algo salió mal y quieres empezar de nuevo:

1. Elimina la carpeta `venv`
2. Elimina la carpeta `data` (si existe)
3. Vuelve al **PASO 2** de esta guía

---

## 📚 ESTRUCTURA DE ARCHIVOS IMPORTANTE

```
sistema-participacion/
│
├── src/
│   ├── main.py              ← INICIA AQUÍ
│   ├── config/
│   │   └── settings.py      ← Configuraciones generales
│   ├── database/
│   │   ├── models.py        ← Modelos de BD
│   │   ├── sqlite_manager.py
│   │   └── sync_manager.py  ← Sincronización
│   ├── ui/
│   │   ├── login_window.py  ← Ventana de login
│   │   └── main_window.py   ← Ventana principal
│   └── controllers/
│       └── auth_controller.py ← Autenticación
│
├── data/
│   └── local.db            ← Base de datos (se crea automáticamente)
│
├── logs/
│   └── app.log             ← Logs de la aplicación
│
├── requirements.txt        ← Dependencias
├── .env                    ← Variables de entorno
├── .env.example            ← Ejemplo de .env
└── run.bat                 ← Ejecutar en Windows (doble clic)
```

---

**¡Todo listo!** 🚀

Si sigues esta guía paso a paso, tu aplicación debería funcionar sin problemas.
