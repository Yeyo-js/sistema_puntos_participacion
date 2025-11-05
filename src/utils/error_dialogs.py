"""
Componentes visuales para mostrar errores de forma amigable
Para usar en las interfaces de CustomTkinter
"""
import customtkinter as ctk
from src.config.settings import COLORS
from typing import Literal


class ErrorDialog(ctk.CTkToplevel):
    """Diálogo para mostrar errores de forma amigable"""
    
    def __init__(self, parent, title: str, message: str, error_type: Literal["error", "warning", "info", "success"] = "error"):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("450x250")
        self.resizable(False, False)
        
        # Configurar colores según tipo
        self.colors = {
            "error": {"icon": "❌", "color": COLORS["danger"], "bg": "#ffe6e6"},
            "warning": {"icon": "⚠️", "color": COLORS["warning"], "bg": "#fff4e6"},
            "info": {"icon": "ℹ️", "color": COLORS["info"], "bg": "#e6f3ff"},
            "success": {"icon": "✅", "color": COLORS["success"], "bg": "#e6ffe6"}
        }
        
        self.error_config = self.colors[error_type]
        self.message = message
        
        self.create_widgets()
        self.center_window()
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
    
    def center_window(self):
        """Centrar ventana"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crear widgets"""
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono
        icon_label = ctk.CTkLabel(
            main_frame,
            text=self.error_config["icon"],
            font=ctk.CTkFont(size=48)
        )
        icon_label.pack(pady=(20, 10))
        
        # Mensaje
        message_label = ctk.CTkLabel(
            main_frame,
            text=self.message,
            font=ctk.CTkFont(size=14),
            text_color=self.error_config["color"],
            wraplength=380,
            justify="center"
        )
        message_label.pack(pady=20, padx=20)
        
        # Botón OK
        ok_button = ctk.CTkButton(
            main_frame,
            text="Entendido",
            width=200,
            height=40,
            command=self.destroy,
            fg_color=self.error_config["color"]
        )
        ok_button.pack(pady=(10, 20))


class InlineErrorMessage(ctk.CTkFrame):
    """Mensaje de error inline (dentro de un formulario)"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=350
        )
        self.label.pack(pady=5)
        
        self.hide()
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        self.label.configure(text=f"❌ {message}", text_color=COLORS["danger"])
        self.pack()
    
    def show_warning(self, message: str):
        """Mostrar advertencia"""
        self.label.configure(text=f"⚠️ {message}", text_color=COLORS["warning"])
        self.pack()
    
    def show_success(self, message: str):
        """Mostrar éxito"""
        self.label.configure(text=f"✅ {message}", text_color=COLORS["success"])
        self.pack()
    
    def show_info(self, message: str):
        """Mostrar información"""
        self.label.configure(text=f"ℹ️ {message}", text_color=COLORS["info"])
        self.pack()
    
    def hide(self):
        """Ocultar mensaje"""
        self.pack_forget()


class Toast(ctk.CTkToplevel):
    """Notificación toast (mensaje temporal en esquina)"""
    
    def __init__(self, parent, message: str, duration: int = 3000, toast_type: Literal["error", "warning", "info", "success"] = "info"):
        super().__init__(parent)
        
        # Configuración de ventana
        self.overrideredirect(True)  # Sin borde
        self.attributes('-topmost', True)  # Siempre al frente
        
        # Colores según tipo
        colors = {
            "error": {"icon": "❌", "bg": COLORS["danger"]},
            "warning": {"icon": "⚠️", "bg": COLORS["warning"]},
            "info": {"icon": "ℹ️", "bg": COLORS["info"]},
            "success": {"icon": "✅", "bg": COLORS["success"]}
        }
        
        config = colors[toast_type]
        
        # Frame principal
        frame = ctk.CTkFrame(
            self,
            fg_color=config["bg"],
            corner_radius=10
        )
        frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Contenido
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)
        
        # Icono
        icon_label = ctk.CTkLabel(
            content_frame,
            text=config["icon"],
            font=ctk.CTkFont(size=20),
            text_color="white"
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Mensaje
        message_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=13),
            text_color="white",
            wraplength=300
        )
        message_label.pack(side="left")
        
        # Posicionar en esquina inferior derecha
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = screen_width - width - 20
        y = screen_height - height - 60
        
        self.geometry(f"+{x}+{y}")
        
        # Auto-cerrar después de duration
        self.after(duration, self.destroy)


# Funciones helper para uso rápido
def show_error(parent, message: str, title: str = "Error"):
    """Mostrar diálogo de error"""
    ErrorDialog(parent, title, message, "error")

def show_warning(parent, message: str, title: str = "Advertencia"):
    """Mostrar diálogo de advertencia"""
    ErrorDialog(parent, title, message, "warning")

def show_info(parent, message: str, title: str = "Información"):
    """Mostrar diálogo de información"""
    ErrorDialog(parent, title, message, "info")

def show_success(parent, message: str, title: str = "Éxito"):
    """Mostrar diálogo de éxito"""
    ErrorDialog(parent, title, message, "success")

def toast_error(parent, message: str):
    """Mostrar toast de error"""
    Toast(parent, message, toast_type="error")

def toast_warning(parent, message: str):
    """Mostrar toast de advertencia"""
    Toast(parent, message, toast_type="warning")

def toast_info(parent, message: str):
    """Mostrar toast de información"""
    Toast(parent, message, toast_type="info")

def toast_success(parent, message: str):
    """Mostrar toast de éxito"""
    Toast(parent, message, toast_type="success")


# ============================================================
# EJEMPLO DE USO EN LOGIN_WINDOW.PY
# ============================================================

"""
# Al inicio del archivo, importar:
from src.utils.error_dialogs import show_error, toast_error, InlineErrorMessage

# En lugar de usar self.message_label.configure(), usar:

# Opción 1: Diálogo modal (para errores importantes)
if not success:
    show_error(self, mensaje, "Error de Registro")
    return

# Opción 2: Toast (notificación temporal, menos invasiva)
if not success:
    toast_error(self, mensaje)
    return

# Opción 3: Mensaje inline (dentro del formulario)
# En create_widgets():
self.error_message = InlineErrorMessage(main_frame)
self.error_message.pack()

# Para mostrar:
self.error_message.show_error("Usuario o contraseña incorrectos")

# Para ocultar:
self.error_message.hide()

# Para éxito:
self.error_message.show_success("Registro exitoso")
"""
