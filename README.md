# 🎓 Sistema de Participación Estudiantil

Sistema de escritorio para gestionar puntos de participación de alumnos con sincronización automática entre SQLite (offline) y SQL Server (online).

## 📋 Características

- ✅ Autenticación de usuarios (profesores)
- ✅ Gestión completa de alumnos (CRUD)
- ✅ Sistema de puntos de participación
- ✅ Organización por ciclos, grados y secciones
- ✅ Funciona offline con SQLite
- ✅ Sincronización automática con SQL Server
- ✅ Exportación e importación de Excel
- ✅ Interfaz moderna con CustomTkinter
- ✅ Sistema de logging completo

## 🚀 Instalación y Configuración

### Paso 1: Clonar o descargar el proyecto

Si estás leyendo esto, ya tienes el proyecto. Si no, descárgalo y extráelo.

### Paso 2: Abrir el proyecto en VS Code

1. Abre **Visual Studio Code**
2. Ve a **File → Open Folder**
3. Selecciona la carpeta `sistema-participacion`

### Paso 3: Crear entorno virtual

Abre la terminal integrada en VS Code (`` Ctrl+` `` o `View → Terminal`) y ejecuta:

**En Windows:**
```bash
python -m venv venv
```

### Paso 4: Activar el entorno virtual

**En Windows (CMD):**
```bash
venv\Scripts\activate
```

**En Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Nota:** Si PowerShell da error de permisos, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Deberías ver `(venv)` al inicio de la línea en tu terminal.

### Paso 5: Instalar dependencias

Con el entorno virtual activado, ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- CustomTkinter (interfaz gráfica moderna)
- SQLAlchemy (ORM para bases de datos)
- pyodbc (driver para SQL Server)
- openpyxl y pandas (manejo de Excel)
- bcrypt (encriptación de contraseñas)
- python-dotenv (variables de entorno)
- colorlog (logs con colores)

### Paso 6: Configurar variables de entorno

1. Copia el archivo `.env.example` y renómbralo a `.env`:
```bash
copy .env.example .env
```

2. Edita el archivo `.env` con tus credenciales de SQL Server (SOLO si vas a usar SQL Server):
```env
SQL_SERVER_HOST=localhost
SQL_SERVER_PORT=1433
SQL_SERVER_DATABASE=sistema_participacion
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=tu_password_aqui
```

**Nota:** El sistema funciona perfectamente sin SQL Server, solo con SQLite (modo offline).

### Paso 7: Configurar SQL Server (OPCIONAL)

Si quieres usar sincronización con SQL Server:

1. Asegúrate de tener SQL Server instalado y corriendo
2. Crea una base de datos llamada `sistema_participacion`
3. Verifica que SQL Server esté aceptando conexiones TCP/IP en el puerto 1433
4. Instala ODBC Driver 17 for SQL Server si no lo tienes:
   - Descárgalo desde: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

**Si NO tienes SQL Server instalado:**
- No hay problema, el sistema funcionará 100% en modo offline con SQLite
- Solo desactiva la sincronización automática poniendo `AUTO_SYNC=False` en el archivo `.env`

## ▶️ Ejecutar la Aplicación

Con el entorno virtual activado, ejecuta:

```bash
python src/main.py
```

### Credenciales por defecto:
- **Email:** `admin@sistema.com`
- **Contraseña:** `admin123`

## 📁 Estructura del Proyecto

```
sistema-participacion/
│
├── src/                          # Código fuente
│   ├── main.py                   # Punto de entrada 🚀
│   ├── config/                   # Configuraciones
│   │   └── settings.py
│   ├── database/                 # Capa de datos
│   │   ├── models.py            # Modelos SQLAlchemy
│   │   ├── sqlite_manager.py    # Gestor SQLite
│   │   ├── sqlserver_manager.py # Gestor SQL Server
│   │   └── sync_manager.py      # Sincronización
│   ├── ui/                       # Interfaz de usuario
│   │   ├── login_window.py      # Ventana de login
│   │   ├── main_window.py       # Ventana principal
│   │   ├── views/               # Vistas específicas
│   │   └── components/          # Componentes reutilizables
│   ├── controllers/              # Lógica de negocio
│   │   └── auth_controller.py
│   └── utils/                    # Utilidades
│       └── logger.py
│
├── data/                         # Base de datos SQLite
│   └── local.db                 # Se crea automáticamente
│
├── exports/                      # Archivos Excel exportados
├── logs/                         # Archivos de log
│   └── app.log
├── requirements.txt              # Dependencias
├── .env                          # Variables de entorno (crear)
├── .env.example                  # Ejemplo de .env
└── README.md                     # Este archivo
```

## 🔧 Desarrollo

### Ver la aplicación mientras desarrollas

La aplicación usa CustomTkinter que muestra ventanas reales. Cada vez que ejecutes `python src/main.py` verás la interfaz gráfica en tiempo real.

### Modificar la interfaz

Los archivos principales de UI son:
- `src/ui/login_window.py` - Ventana de login
- `src/ui/main_window.py` - Ventana principal con navegación

### Base de datos

El proyecto usa SQLAlchemy ORM. Los modelos están en `src/database/models.py`:
- Usuario (profesores)
- Institucion (colegios/institutos)
- Nivel (ciclos/grados)
- Seccion (A, B, C, etc.)
- Clase (cursos que dicta el profesor)
- Alumno
- Participacion (puntos)
- SyncLog (registro de sincronizaciones)

### Logging

Los logs se guardan en `logs/app.log` y se muestran en la consola con colores.

Nivel de detalle controlado por `DEBUG=True/False` en `.env`

## 🔄 Sincronización

### Automática
- Se ejecuta cada 5 minutos por defecto (configurable en `.env`)
- Sube cambios de SQLite a SQL Server
- Solo funciona si SQL Server está disponible

### Manual
- Click en el botón "🔄 Sincronizar Ahora" en la barra lateral
- Sincronización bidireccional

### Modo Offline
- Si SQL Server no está disponible, el sistema funciona 100% con SQLite
- Los datos se sincronizan automáticamente cuando SQL Server vuelva a estar disponible

## 📦 Próximas Funcionalidades

- [ ] CRUD completo de alumnos
- [ ] Asignación de puntos de participación
- [ ] Importación masiva desde Excel
- [ ] Exportación de reportes a Excel
- [ ] Gestión de clases y secciones
- [ ] Dashboard con estadísticas
- [ ] Búsqueda y filtros avanzados
- [ ] Historial de cambios
- [ ] Respaldo y restauración de datos

## ❓ Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "No module named 'src'"
Asegúrate de ejecutar desde la carpeta raíz del proyecto:
```bash
cd sistema-participacion
python src/main.py
```

### Error con SQL Server
- Verifica que SQL Server esté corriendo
- Verifica las credenciales en `.env`
- Verifica que ODBC Driver 17 esté instalado
- Si no puedes resolverlo, pon `AUTO_SYNC=False` en `.env` y usa solo SQLite

### La ventana no aparece
- Verifica que tengas instalado Python 3.8 o superior
- Reinstala las dependencias: `pip install -r requirements.txt --force-reinstall`

## 📝 Notas Adicionales

- **Base de datos:** SQLite se crea automáticamente en `data/local.db`
- **Logs:** Revisa `logs/app.log` para ver el historial completo
- **Tema:** La aplicación usa tema oscuro por defecto (configurable en `settings.py`)
- **Windows:** Optimizado para Windows, pero compatible con Linux/Mac

## 🤝 Contribuciones

Este es tu proyecto personal. Siéntete libre de modificar y extender según tus necesidades.

## 📄 Licencia

Proyecto de uso personal y educativo.

---

**¡Listo para comenzar!** 🚀

Ejecuta `python src/main.py` y empieza a desarrollar tu sistema.
