# 🚀 GUÍA DE INICIO RÁPIDO

## ⚡ Instalación en 3 pasos (Windows)

### 1️⃣ Instalar automáticamente

Haz doble clic en `install.bat` y espera a que termine.

### 2️⃣ Configurar (opcional)

Edita el archivo `.env` si vas a usar SQL Server (modo online).

### 3️⃣ Ejecutar

Haz doble clic en `run.bat`

---

## 📋 Instalación Manual

### Paso 1: Crear entorno virtual

```bash
python -m venv venv
```

### Paso 2: Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar

```bash
# Copiar archivo de configuración
copy .env.example .env

# Editar .env con tu configuración (opcional)
```

### Paso 5: Ejecutar

```bash
python src/main.py
```

---

## 👤 Primer Usuario

1. Ejecuta la aplicación
2. Clic en "Registrar Nuevo Usuario"
3. Completa el formulario:
   - **Nombre Completo:** Tu nombre
   - **Usuario:** elige un usuario
   - **Email:** (opcional)
   - **Contraseña:** mínimo 6 caracteres
4. Clic en "Registrar"
5. Inicia sesión con tus credenciales

---

## 💡 Características Principales

### ✅ Ya Implementado

- ✅ Sistema de login y registro
- ✅ Dashboard principal
- ✅ Base de datos SQLite (offline)
- ✅ Sincronización con SQL Server (online)
- ✅ Interfaz moderna con CustomTkinter
- ✅ Sistema de logging

### 🚧 En Desarrollo

- 🚧 CRUD de estudiantes
- 🚧 Registro de participaciones
- 🚧 Gestión de clases
- 🚧 Exportación a Excel
- 🚧 Reportes y estadísticas

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: "Python no está instalado"

**Solución:** Instala Python desde https://www.python.org/downloads/

### ❌ Error: "No module named 'customtkinter'"

**Solución:**
```bash
venv\Scripts\activate
pip install customtkinter
```

### ❌ La ventana no aparece

**Solución:**
1. Cierra todos los procesos de Python
2. Vuelve a ejecutar `run.bat`

### ❌ Error de base de datos

**Solución:**
1. Elimina la carpeta `data/`
2. Vuelve a ejecutar la aplicación (se creará automáticamente)

---

## 📁 Archivos Importantes

```
sistema-participacion/
│
├── install.bat          ← Instalador automático (Windows)
├── run.bat             ← Ejecutar aplicación (Windows)
├── requirements.txt    ← Dependencias de Python
├── .env                ← Configuración (crear desde .env.example)
├── README.md           ← Documentación completa
│
├── src/
│   └── main.py         ← Archivo principal
│
├── data/
│   └── local.db        ← Base de datos SQLite (se crea automáticamente)
│
└── logs/
    └── app.log         ← Logs de la aplicación
```

---

## 🎯 Próximos Pasos

1. **Explora el Dashboard**
   - Verás las diferentes secciones del sistema

2. **Configura tus Clases**
   - Ve a la sección "Clases"
   - Crea tus primeras clases/cursos

3. **Agrega Estudiantes**
   - Ve a la sección "Estudiantes"
   - Agrega estudiantes uno por uno o importa desde Excel

4. **Registra Participaciones**
   - Ve a la sección "Participaciones"
   - Asigna puntos a tus estudiantes

5. **Genera Reportes**
   - Ve a la sección "Reportes"
   - Exporta datos a Excel

---

## 📞 ¿Necesitas Ayuda?

- 📖 Lee el **README.md** completo para más detalles
- 📝 Revisa los logs en `logs/app.log` si hay errores
- 🔍 Busca en la documentación de Python y CustomTkinter

---

**¡Disfruta usando el Sistema de Puntos de Participación!** 🎓
