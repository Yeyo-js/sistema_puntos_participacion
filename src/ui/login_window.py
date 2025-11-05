"""
Ventana de Login MEJORADA - VERSIÓN FINAL PERFECTA
Con botón mostrar contraseña DENTRO del input y sin mensajes de texto
"""
import customtkinter as ctk
from src.controllers.auth_controller import auth_controller
from src.config.settings import APP_NAME, UI_THEME, COLORS
from src.utils.session_manager import session_manager
from src.utils.error_dialogs import show_error, show_success, show_warning
import logging

logger = logging.getLogger(__name__)


class PasswordEntry(ctk.CTkFrame):
    """Entry personalizado para contraseña con botón mostrar/ocultar integrado"""
    
    def __init__(self, parent, placeholder_text="Contraseña", width=400, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.password_visible = False
        
        # Frame que simula un input (con borde)
        self.entry_frame = ctk.CTkFrame(
            self,
            fg_color=("#F9F9FA", "#343638"),
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            width=width,
            height=40
        )
        self.entry_frame.pack(fill="both", expand=True)
        self.entry_frame.pack_propagate(False)
        
        # Entry sin borde (dentro del frame)
        self.entry = ctk.CTkEntry(
            self.entry_frame,
            placeholder_text=placeholder_text,
            show="*",
            width=width-50,
            height=40,  # ← CAMBIO: de 36 a 40 (altura completa)
            border_width=0,
            fg_color="transparent",
            font=ctk.CTkFont(size=14)
        )
        self.entry.place(x=8, y=0)  # ← CAMBIO: usar place en vez de pack
        
        # Botón mostrar/ocultar (dentro del frame) - CENTRADO ABSOLUTO
        self.toggle_btn = ctk.CTkButton(
            self.entry_frame,
            text="👁️",
            width=40,  # ← CAMBIO: de 30 a 40
            height=40,  # ← CAMBIO: altura completa
            command=self.toggle_visibility,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            corner_radius=6,
            font=ctk.CTkFont(size=18)  # ← CAMBIO: de 16 a 18
        )
        self.toggle_btn.place(x=width-45, y=0)  # ← CAMBIO: usar place para posición exacta
    
    def toggle_visibility(self):
        """Alternar visibilidad de contraseña"""
        if self.password_visible:
            self.entry.configure(show="*")
            self.toggle_btn.configure(text="👁️")
            self.password_visible = False
        else:
            self.entry.configure(show="")
            self.toggle_btn.configure(text="🙈")
            self.password_visible = True
    
    def get(self):
        """Obtener texto del entry"""
        return self.entry.get()
    
    def focus(self):
        """Dar foco al entry"""
        self.entry.focus()
    
    def bind(self, *args, **kwargs):
        """Pasar bind al entry interno"""
        return self.entry.bind(*args, **kwargs)
    
    def toggle_visibility(self):
        """Alternar visibilidad de contraseña"""
        if self.password_visible:
            self.entry.configure(show="*")
            self.toggle_btn.configure(text="👁️")
            self.password_visible = False
        else:
            self.entry.configure(show="")
            self.toggle_btn.configure(text="🙈")
            self.password_visible = True
    
    def get(self):
        """Obtener texto del entry"""
        return self.entry.get()
    
    def focus(self):
        """Dar foco al entry"""
        self.entry.focus()
    
    def bind(self, *args, **kwargs):
        """Pasar bind al entry interno"""
        return self.entry.bind(*args, **kwargs)


class LoginWindow(ctk.CTk):
    """Ventana de inicio de sesión mejorada"""
    
    def __init__(self):
        super().__init__()
        
        self.usuario_autenticado = None
        
        # Configuración de la ventana
        self.title(f"{APP_NAME} - Login")
        self.geometry("550x650")
        self.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(UI_THEME)
        
        # Intentar auto-login
        if self.try_auto_login():
            return
        
        # Si hay PIN, mostrar login rápido
        if session_manager.has_pin():
            self.create_pin_login()
        else:
            self.create_normal_login()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def try_auto_login(self):
        """Intentar auto-login con sesión guardada"""
        success, usuario, mensaje = auth_controller.auto_login()
        
        if success:
            logger.info("Auto-login exitoso")
            self.usuario_autenticado = usuario
            self.after(100, self.open_main_window)
            return True
        
        return False
    
    def create_pin_login(self):
        """Crear interfaz de login rápido con PIN"""
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
            text="Acceso Rápido",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame de PIN
        pin_frame = ctk.CTkFrame(main_frame)
        pin_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        pin_label = ctk.CTkLabel(
            pin_frame,
            text="🔒 Ingresa tu PIN",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        pin_label.pack(pady=(30, 20))
        
        self.pin_entry = ctk.CTkEntry(
            pin_frame,
            placeholder_text="PIN de 4 dígitos",
            show="●",
            width=200,
            height=50,
            font=ctk.CTkFont(size=24),
            justify="center"
        )
        self.pin_entry.pack(pady=20)
        self.pin_entry.bind('<KeyRelease>', self.on_pin_key)
        
        self.pin_login_button = ctk.CTkButton(
            pin_frame,
            text="Ingresar",
            command=self.handle_pin_login,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pin_login_button.pack(pady=10)
        
        separator = ctk.CTkFrame(pin_frame, height=2)
        separator.pack(fill="x", padx=50, pady=20)
        
        full_login_button = ctk.CTkButton(
            pin_frame,
            text="Usar Usuario y Contraseña",
            command=self.switch_to_normal_login,
            width=250,
            height=35,
            fg_color="transparent",
            border_width=2
        )
        full_login_button.pack(pady=(10, 30))
        
        self.pin_entry.focus()
    
    def create_normal_login(self):
        """Crear interfaz de login normal"""
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
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame de login
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Iniciar Sesión",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        login_label.pack(pady=(30, 30))
        
        # Usuario
        self.username_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Nombre de Usuario",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=10)
        
        # Password con botón integrado
        self.password_field = PasswordEntry(login_frame, width=400)
        self.password_field.pack(pady=10)
        
        # Checkbox "Recordarme"
        self.remember_var = ctk.BooleanVar(value=False)
        self.remember_checkbox = ctk.CTkCheckBox(
            login_frame,
            text="Recordarme (mantener sesión por 7 días)",
            variable=self.remember_var,
            font=ctk.CTkFont(size=12)
        )
        self.remember_checkbox.pack(pady=10)
        
        # Botón de login
        self.login_button = ctk.CTkButton(
            login_frame,
            text="Iniciar Sesión",
            command=self.handle_login,
            width=400,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.login_button.pack(pady=20)
        
        # Separador
        separator = ctk.CTkFrame(login_frame, height=2)
        separator.pack(fill="x", padx=50, pady=15)
        
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
            text="Usuario por defecto: admin | Contraseña: admin123",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(pady=(0, 10))
        
        # Bind Enter key
        self.password_field.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.bind("<Return>", lambda e: self.password_field.focus())
        
        # Focus en primer campo
        self.username_entry.focus()
    
    def switch_to_normal_login(self):
        """Cambiar a login normal"""
        for widget in self.winfo_children():
            widget.destroy()
        self.create_normal_login()
    
    def on_pin_key(self, event):
        """Manejar tecla presionada en PIN"""
        pin = self.pin_entry.get()
        
        if len(pin) > 4:
            self.pin_entry.delete(4, 'end')
            pin = pin[:4]
        
        if pin and not pin.isdigit():
            self.pin_entry.delete(0, 'end')
            return
        
        if len(pin) == 4:
            self.after(200, self.handle_pin_login)
    
    def handle_pin_login(self):
        """Manejar login con PIN"""
        pin = self.pin_entry.get().strip()
        
        if len(pin) != 4:
            show_warning(self, "El PIN debe tener exactamente 4 dígitos", "PIN Inválido")
            return
        
        self.pin_entry.configure(state="disabled")
        self.pin_login_button.configure(state="disabled", text="Verificando...")
        self.update()
        
        success, usuario, mensaje = auth_controller.login_with_pin(pin)
        
        if success:
            self.usuario_autenticado = usuario
            logger.info(f"Login con PIN exitoso")
            self.after(500, self.open_main_window)
        else:
            mensaje_limpio = mensaje.replace("❌ ", "")
            show_error(self, mensaje_limpio, "Error de Autenticación")
            self.pin_entry.configure(state="normal")
            self.pin_entry.delete(0, 'end')
            self.pin_login_button.configure(state="normal", text="Ingresar")
            self.pin_entry.focus()
    
    def handle_login(self):
        """Manejar el evento de login"""
        username = self.username_entry.get().strip()
        password = self.password_field.get()
        remember_me = self.remember_var.get()
        
        if not username or not password:
            show_warning(self, "Por favor ingresa tu usuario y contraseña para continuar.", "Campos Vacíos")
            return
        
        self.login_button.configure(state="disabled", text="Iniciando sesión...")
        self.update()
        
        success, usuario, mensaje = auth_controller.login(username, password, remember_me)
        
        if success:
            self.usuario_autenticado = usuario
            logger.info(f"Login exitoso para: {username}")
            
            if remember_me and not session_manager.has_pin():
                self.after(100, self.offer_pin_setup)
            else:
                self.after(100, self.open_main_window)
        else:
            mensaje_limpio = mensaje.replace("❌ ", "").replace("⏳ ", "").replace("🚫 ", "").replace("⚠️ ", "")
            
            if "bloqueado" in mensaje.lower() or "espera" in mensaje.lower():
                show_warning(self, mensaje_limpio, "Cuenta Bloqueada Temporalmente")
            else:
                show_error(self, mensaje_limpio, "Error de Autenticación")
            
            self.login_button.configure(state="normal", text="Iniciar Sesión")
    
    def offer_pin_setup(self):
        """Ofrecer configurar PIN para acceso rápido"""
        dialog = PinSetupDialog(self)
        dialog.grab_set()
        self.wait_window(dialog)
        self.open_main_window()
    
    def open_register(self):
        """Abrir ventana de registro"""
        RegisterWindow(self)
    
    def open_main_window(self):
        """Abrir ventana principal de la aplicación"""
        self.destroy()
        from src.ui.main_window import MainWindow
        app = MainWindow(self.usuario_autenticado)
        app.mainloop()


class PinSetupDialog(ctk.CTkToplevel):
    """Diálogo para configurar PIN de acceso rápido"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Configurar PIN Rápido")
        self.geometry("450x400")
        self.resizable(False, False)
        
        self.create_widgets()
        self.center_window()
    
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
        
        title = ctk.CTkLabel(
            main_frame,
            text="🔒 Configurar PIN Rápido",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        desc = ctk.CTkLabel(
            main_frame,
            text="Configura un PIN de 4 dígitos para\nacceder más rápido la próxima vez",
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        desc.pack(pady=(0, 30))
        
        ctk.CTkLabel(
            main_frame,
            text="Ingresa tu PIN (4 dígitos):",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(10, 5))
        
        self.pin_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="0000",
            show="●",
            width=200,
            height=50,
            font=ctk.CTkFont(size=24),
            justify="center"
        )
        self.pin_entry.pack(pady=10)
        self.pin_entry.bind('<KeyRelease>', self.validate_pin_input)
        
        ctk.CTkLabel(
            main_frame,
            text="Confirma tu PIN:",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(20, 5))
        
        self.pin_confirm_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="0000",
            show="●",
            width=200,
            height=50,
            font=ctk.CTkFont(size=24),
            justify="center"
        )
        self.pin_confirm_entry.pack(pady=10)
        self.pin_confirm_entry.bind('<KeyRelease>', self.validate_pin_input)
        
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        skip_btn = ctk.CTkButton(
            buttons_frame,
            text="Omitir",
            width=180,
            height=40,
            command=self.destroy,
            fg_color="gray"
        )
        skip_btn.pack(side="left", padx=10)
        
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar PIN",
            width=180,
            height=40,
            command=self.save_pin,
            fg_color="green"
        )
        self.save_btn.pack(side="right", padx=10)
        
        self.pin_entry.focus()
    
    def validate_pin_input(self, event):
        """Validar entrada de PIN"""
        pin1 = self.pin_entry.get()
        if len(pin1) > 4:
            self.pin_entry.delete(4, 'end')
        if pin1 and not pin1.isdigit():
            self.pin_entry.delete(len(pin1)-1, 'end')
        
        pin2 = self.pin_confirm_entry.get()
        if len(pin2) > 4:
            self.pin_confirm_entry.delete(4, 'end')
        if pin2 and not pin2.isdigit():
            self.pin_confirm_entry.delete(len(pin2)-1, 'end')
    
    def save_pin(self):
        """Guardar PIN"""
        pin = self.pin_entry.get()
        pin_confirm = self.pin_confirm_entry.get()
        
        if len(pin) != 4:
            show_warning(self, "El PIN debe tener exactamente 4 dígitos", "PIN Inválido")
            return
        
        if pin != pin_confirm:
            show_error(self, "Los PINs no coinciden. Por favor verifica e intenta de nuevo.", "Error de Validación")
            return
        
        valid, mensaje = auth_controller.validate_pin(pin)
        if not valid:
            show_error(self, mensaje.replace("❌ ", ""), "PIN Débil")
            return
        
        session_data = session_manager.load_session()
        if not session_data:
            show_error(self, "No se pudo guardar el PIN. Intenta iniciar sesión de nuevo.", "Error del Sistema")
            return
        
        success, msg = auth_controller.setup_pin(session_data['username'], pin)
        
        if success:
            show_success(self, "Tu PIN ha sido configurado exitosamente", "PIN Configurado")
            self.after(1000, self.destroy)
        else:
            show_error(self, msg.replace("❌ ", ""), "Error al Guardar PIN")


class RegisterWindow(ctk.CTkToplevel):
    """Ventana de registro MEJORADA"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title(f"{APP_NAME} - Registro")
        self.geometry("500x700")
        self.resizable(False, False)
        
        self.center_window()
        self.create_widgets()
        
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
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.nombre_entry.pack(pady=10)
        
        # Usuario
        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Nombre de usuario (ej: jperez)",
            width=400,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=10)
        
        username_hint = ctk.CTkLabel(
            main_frame,
            text="Solo letras, números y guiones bajos (3-20 caracteres)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        username_hint.pack(pady=(0, 10))
        
        # Contraseña con botón integrado
        self.password_field = PasswordEntry(main_frame, "Contraseña", width=400)
        self.password_field.pack(pady=10)
        
        password_hint = ctk.CTkLabel(
            main_frame,
            text="Mínimo 6 caracteres, debe incluir letras y números",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        password_hint.pack(pady=(0, 10))
        
        # Confirmar contraseña con botón integrado
        self.confirm_password_field = PasswordEntry(main_frame, "Confirmar contraseña", width=400)
        self.confirm_password_field.pack(pady=10)
        
        # Botón de registro
        self.register_button = ctk.CTkButton(
            main_frame,
            text="Registrarse",
            command=self.handle_register,
            width=400,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.register_button.pack(pady=(30, 10))
        
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
        """Manejar registro"""
        nombre = self.nombre_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_field.get()
        confirm_password = self.confirm_password_field.get()
        
        if not nombre or not username or not password or not confirm_password:
            show_error(self, "Por favor complete todos los campos", "Campos Incompletos")
            return
        
        if password != confirm_password:
            show_error(self, "Las contraseñas no coinciden. Por favor verifica e intenta de nuevo.", "Error de Validación")
            return
        
        self.register_button.configure(state="disabled", text="Registrando...")
        self.update()
        
        success, mensaje = auth_controller.register(nombre, username, password)
        
        if success:
            show_success(self, mensaje.replace("✅ ", ""), "Registro Exitoso")
            logger.info(f"Nuevo usuario registrado: {username}")
            self.after(500, self.destroy)
        else:
            mensaje_limpio = mensaje.replace("❌ ", "")
            show_error(self, mensaje_limpio, "Error de Registro")
            self.register_button.configure(state="normal", text="Registrarse")
