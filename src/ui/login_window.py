"""
Ventana de inicio de sesión
"""
import customtkinter as ctk
from src.controllers.auth_controller import auth_controller
from src.config.settings import APP_NAME, UI_THEME
import logging

logger = logging.getLogger(__name__)


class LoginWindow(ctk.CTk):
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        super().__init__()
        
        self.usuario_autenticado = None
        
        # Configuración de la ventana
        self.title(f"{APP_NAME} - Login")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(UI_THEME)
        
        # Crear interfaz
        self.create_widgets()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=APP_NAME,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(40, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Sistema de Gestión de Participación Estudiantil",
            font=ctk.CTkFont(size=12)
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame de login
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Label de login
        login_label = ctk.CTkLabel(
            login_frame,
            text="Iniciar Sesión",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        login_label.pack(pady=(30, 30))
        
        # Email
        self.email_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Email",
            width=300,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(pady=10)
        
        # Password
        self.password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Contraseña",
            show="*",
            width=300,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=10)
        
        # Botón de login
        self.login_button = ctk.CTkButton(
            login_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.login_button.pack(pady=20)
        
        # Label de error/mensaje
        self.message_label = ctk.CTkLabel(
            login_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.message_label.pack(pady=10)
        
        # Separador
        separator = ctk.CTkFrame(login_frame, height=2)
        separator.pack(fill="x", padx=50, pady=20)
        
        # Link de registro
        register_label = ctk.CTkLabel(
            login_frame,
            text="¿No tienes cuenta?",
            font=ctk.CTkFont(size=12)
        )
        register_label.pack(pady=(10, 5))
        
        register_button = ctk.CTkButton(
            login_frame,
            text="Registrarse",
            command=self.open_register,
            width=200,
            height=35,
            fg_color="transparent",
            border_width=2
        )
        register_button.pack(pady=(0, 30))
        
        # Información de admin por defecto
        info_label = ctk.CTkLabel(
            main_frame,
            text="Usuario por defecto: admin@sistema.com | Contraseña: admin123",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(pady=(0, 10))
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
    
    def handle_login(self):
        """Manejar el evento de login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validaciones básicas
        if not email or not password:
            self.show_message("Por favor complete todos los campos", "red")
            return
        
        # Deshabilitar botón durante el login
        self.login_button.configure(state="disabled", text="Iniciando sesión...")
        self.update()
        
        # Intentar autenticar
        success, usuario, mensaje = auth_controller.login(email, password)
        
        if success:
            self.usuario_autenticado = usuario
            self.show_message("Login exitoso", "green")
            logger.info(f"Login exitoso para: {email}")
            
            # Cerrar ventana de login y abrir ventana principal
            self.after(500, self.open_main_window)
        else:
            self.show_message(mensaje, "red")
            self.login_button.configure(state="normal", text="Iniciar Sesión")
    
    def show_message(self, message: str, color: str):
        """Mostrar mensaje en la interfaz"""
        self.message_label.configure(text=message, text_color=color)
    
    def open_register(self):
        """Abrir ventana de registro"""
        RegisterWindow(self)
    
    def open_main_window(self):
        """Abrir ventana principal de la aplicación"""
        self.destroy()
        from src.ui.main_window import MainWindow
        app = MainWindow(self.usuario_autenticado)
        app.mainloop()


class RegisterWindow(ctk.CTkToplevel):
    """Ventana de registro de nuevos usuarios"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title(f"{APP_NAME} - Registro")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Crear interfaz
        self.create_widgets()
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Crear Nueva Cuenta",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(30, 40))
        
        # Nombre completo
        self.nombre_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Nombre completo",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.nombre_entry.pack(pady=10)
        
        # Email
        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Email",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(pady=10)
        
        # Contraseña
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Contraseña",
            show="*",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(pady=10)
        
        # Confirmar contraseña
        self.confirm_password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Confirmar contraseña",
            show="*",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.confirm_password_entry.pack(pady=10)
        
        # Botón de registro
        self.register_button = ctk.CTkButton(
            main_frame,
            text="Registrarse",
            command=self.handle_register,
            width=350,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.register_button.pack(pady=30)
        
        # Label de mensaje
        self.message_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.message_label.pack(pady=10)
        
        # Botón cancelar
        cancel_button = ctk.CTkButton(
            main_frame,
            text="Cancelar",
            command=self.destroy,
            width=200,
            height=35,
            fg_color="transparent",
            border_width=2
        )
        cancel_button.pack(pady=10)
    
    def handle_register(self):
        """Manejar el evento de registro"""
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validaciones
        if not nombre or not email or not password or not confirm_password:
            self.show_message("Por favor complete todos los campos", "red")
            return
        
        if password != confirm_password:
            self.show_message("Las contraseñas no coinciden", "red")
            return
        
        if len(password) < 6:
            self.show_message("La contraseña debe tener al menos 6 caracteres", "red")
            return
        
        # Deshabilitar botón durante el registro
        self.register_button.configure(state="disabled", text="Registrando...")
        self.update()
        
        # Intentar registrar
        success, mensaje = auth_controller.register(nombre, email, password)
        
        if success:
            self.show_message("Registro exitoso", "green")
            logger.info(f"Nuevo usuario registrado: {email}")
            self.after(1500, self.destroy)
        else:
            self.show_message(mensaje, "red")
            self.register_button.configure(state="normal", text="Registrarse")
    
    def show_message(self, message: str, color: str):
        """Mostrar mensaje en la interfaz"""
        self.message_label.configure(text=message, text_color=color)
