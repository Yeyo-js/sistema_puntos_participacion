# 📚 ÍNDICE DE DOCUMENTOS

Bienvenido al Sistema de Participación Estudiantil. Esta guía te ayudará a saber qué documento leer primero.

---

## 🎯 ¿QUÉ DOCUMENTO LEER?

### 👉 **EMPIEZA AQUÍ** (Si eres nuevo)

**1. QUICK_START.md** ⚡
- Solo 3 comandos
- 5 minutos
- Para instalación express

**2. RESUMEN.md** 📋
- Vista general del proyecto
- Qué incluye
- Características implementadas

---

### 📖 **INSTALACIÓN DETALLADA**

**3. GUIA_INICIO.md** 📘
- Paso a paso completo
- Con screenshots mentales
- Solución de problemas
- Recomendado si tienes dudas

---

### 📚 **DOCUMENTACIÓN COMPLETA**

**4. README.md** 📖
- Documentación técnica completa
- Estructura del proyecto
- Funcionalidades
- Para referencia

---

## 🚀 ARCHIVOS EJECUTABLES

### Windows:

**install.bat** 🔧
- Instalación automática
- Crea entorno virtual
- Instala dependencias
- Doble clic y listo

**run.bat** ▶️
- Ejecuta la aplicación
- Usa después de instalar
- Doble clic para abrir

---

## 📝 ARCHIVOS DE CONFIGURACIÓN

**.env** ⚙️
- Variables de entorno
- Ya está configurado
- Editar solo si usas SQL Server

**.env.example** 📄
- Ejemplo de configuración
- Para referencia

**requirements.txt** 📦
- Lista de dependencias
- Usado por pip

**.gitignore** 🚫
- Archivos ignorados por Git

---

## 🗂️ ESTRUCTURA DE CARPETAS

```
sistema-participacion/
│
├── 📄 DOCUMENTACIÓN
│   ├── QUICK_START.md      ← Inicio en 5 min ⚡
│   ├── RESUMEN.md          ← Vista general 📋
│   ├── GUIA_INICIO.md      ← Paso a paso 📘
│   └── README.md           ← Documentación completa 📖
│
├── 🚀 EJECUTABLES
│   ├── install.bat         ← Instalar (doble clic)
│   └── run.bat             ← Ejecutar (doble clic)
│
├── 🔧 CONFIGURACIÓN
│   ├── .env                ← Variables de entorno
│   ├── .env.example        ← Ejemplo
│   ├── requirements.txt    ← Dependencias
│   └── .gitignore          ← Git ignore
│
├── 🐍 CÓDIGO FUENTE
│   └── src/
│       ├── main.py                 ← INICIO AQUÍ
│       ├── config/settings.py      ← Configuración
│       ├── database/               ← BD y modelos
│       ├── controllers/            ← Lógica de negocio
│       ├── ui/                     ← Interfaz gráfica
│       └── utils/                  ← Utilidades
│
└── 📁 DATOS
    ├── data/               ← Base de datos SQLite
    ├── exports/            ← Excel exportados
    ├── logs/               ← Archivos de log
    └── assets/             ← Recursos
```

---

## 🎓 FLUJO DE LECTURA RECOMENDADO

### Para Principiantes:
1. **QUICK_START.md** - Instalar rápido
2. **RESUMEN.md** - Entender el proyecto
3. **Ejecutar la app** - Explorar la interfaz
4. **GUIA_INICIO.md** - Si hay problemas

### Para Desarrolladores:
1. **RESUMEN.md** - Vista general
2. **README.md** - Documentación técnica
3. **src/database/models.py** - Ver modelos
4. **src/ui/main_window.py** - Ver interfaz
5. **Empezar a codear** 🚀

---

## ⚡ INICIO ULTRA RÁPIDO

### Método 1: Doble Clic (Windows)
```
1. Doble clic en install.bat
2. Esperar 3-5 minutos
3. Doble clic en run.bat
```

### Método 2: Terminal (3 comandos)
```bash
python -m venv venv
venv\Scripts\activate && pip install -r requirements.txt
python src/main.py
```

**Login:** admin@sistema.com / admin123

---

## 🆘 AYUDA

### Problemas de instalación:
→ Lee **GUIA_INICIO.md** sección "Problemas Comunes"

### Entender el proyecto:
→ Lee **RESUMEN.md**

### Documentación técnica:
→ Lee **README.md**

### Errores en ejecución:
→ Revisa **logs/app.log**

---

## 📞 SOPORTE

Si algo no funciona:

1. ✅ Verifica que Python esté instalado
2. ✅ Lee GUIA_INICIO.md
3. ✅ Revisa logs/app.log
4. ✅ Intenta reinstalar: `pip install -r requirements.txt --force-reinstall`

---

## 🎉 TODO LISTO

Ahora sabes qué leer y en qué orden.

**Recomendación:** Empieza por **QUICK_START.md** y luego **RESUMEN.md**

---

**¡Éxito con tu proyecto!** 🚀

---

## 📋 CHECKLIST RÁPIDO

- [ ] Leí QUICK_START.md
- [ ] Instalé las dependencias (install.bat)
- [ ] Ejecuté la aplicación (run.bat)
- [ ] Hice login con admin@sistema.com
- [ ] Exploré la interfaz
- [ ] Leí RESUMEN.md
- [ ] Estoy listo para desarrollar ✨

---

Última actualización: 2025
