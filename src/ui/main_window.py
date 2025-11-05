"""
Ventana principal de la aplicación
"""
import customtkinter as ctk
from src.config.settings import APP_NAME, APP_VERSION, WINDOW_SIZE, MIN_WINDOW_SIZE, UI_THEME
from src.database.sync_manager import sync_manager
from src.ui.views.students_view import StudentsView
import logging

logger = logging.getLogger(__name__)


class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación"""
    
    def __init__(self, usuario):
        super().__init__()
        
        self.usuario = usuario
        
        # Configuración de la ventana
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.minsize(*MIN_WINDOW_SIZE)

        # Abrir en 90% de la pantalla CENTRADA
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)

        # Calcular posición centrada
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Aplicar geometría centrada
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(UI_THEME)
        
        # Variables de estado
        self.current_view = None
        
        # Crear interfaz
        self.create_widgets()
        
        # Iniciar sincronización automática
        sync_manager.start_auto_sync()
        
        # Protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        logger.info(f"Ventana principal iniciada para usuario: {usuario.nombre}")
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        """Crear los widgets de la interfaz"""
        
        # Grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Mostrar dashboard por defecto
        self.show_dashboard()
    
    def create_sidebar(self):
        """Crear barra lateral de navegación"""
        
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Título
        logo_label = ctk.CTkLabel(
            self.sidebar,
            text=APP_NAME,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Usuario
        user_frame = ctk.CTkFrame(self.sidebar)
        user_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.usuario.nombre}",
            font=ctk.CTkFont(size=12)
        )
        user_label.pack(pady=10)
        
        # Separador
        separator1 = ctk.CTkFrame(self.sidebar, height=2)
        separator1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Botones de navegación
        self.nav_buttons = {}
        
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("👥 Alumnos", "students"),
            ("⭐ Participación", "points"),
            ("📚 Clases", "classes"),
            ("📈 Reportes", "reports"),
            ("⚙️ Configuración", "settings"),
        ]
        
        for idx, (text, view_name) in enumerate(nav_items, start=3):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda v=view_name: self.change_view(v),
                anchor="w",
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.grid(row=idx, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons[view_name] = btn
        
        # Separador
        separator2 = ctk.CTkFrame(self.sidebar, height=2)
        separator2.grid(row=9, column=0, padx=20, pady=10, sticky="ew")
        
        # Botón de sincronización
        self.sync_button = ctk.CTkButton(
            self.sidebar,
            text="🔄 Sincronizar Ahora",
            command=self.manual_sync,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        self.sync_button.grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        
        # Botón de cerrar sesión
        logout_button = ctk.CTkButton(
            self.sidebar,
            text="🚪 Cerrar Sesión",
            command=self.logout,
            height=40,
            fg_color="transparent",
            border_width=2
        )
        logout_button.grid(row=11, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Estado de sincronización
        self.sync_status_label = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.sync_status_label.grid(row=12, column=0, padx=20, pady=(0, 10))
    
    def change_view(self, view_name: str):
        """Cambiar la vista actual"""
        
        # Limpiar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Actualizar estado de botones
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == view_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=("gray85", "gray20"))
        
        self.current_view = view_name
        
        # Mostrar la vista correspondiente
        if view_name == "dashboard":
            self.show_dashboard()
        elif view_name == "students":
            self.show_students()
        elif view_name == "points":
            self.show_points()
        elif view_name == "classes":
            self.show_classes()
        elif view_name == "reports":
            self.show_reports()
        elif view_name == "settings":
            self.show_settings()
    
    def show_dashboard(self):
        """Mostrar dashboard"""
        title = ctk.CTkLabel(
            self.main_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Tarjetas de información
        cards_frame = ctk.CTkFrame(self.main_frame)
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # Grid de 3 columnas
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Tarjeta 1: Total de clases
        card1 = self.create_info_card(cards_frame, "Mis Clases", "0", "📚")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Tarjeta 2: Total de alumnos
        card2 = self.create_info_card(cards_frame, "Total Alumnos", "0", "👥")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Tarjeta 3: Participaciones hoy
        card3 = self.create_info_card(cards_frame, "Participaciones Hoy", "0", "⭐")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Bienvenida
        welcome_frame = ctk.CTkFrame(self.main_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text=f"¡Bienvenido de nuevo, {self.usuario.nombre}!",
            font=ctk.CTkFont(size=20)
        )
        welcome_text.pack(pady=30)
        
        info_text = ctk.CTkLabel(
            welcome_frame,
            text="Selecciona una opción del menú lateral para comenzar.",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_text.pack(pady=10)
    
    def create_info_card(self, parent, title, value, icon):
        """Crear tarjeta de información"""
        card = ctk.CTkFrame(parent)
        
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=40)
        )
        icon_label.pack(pady=(20, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        value_label.pack(pady=5)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        title_label.pack(pady=(5, 20))
        
        return card
    
    def clear_content(self):
        """Limpiar el frame de contenido"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_students(self):
        """Mostrar vista de Estudiantes"""
        self.clear_content()
        
        # Crear y mostrar la vista de estudiantes
        students_view = StudentsView(self.main_frame)
        students_view.pack(fill="both", expand=True)
        
        logger.info("Vista Estudiantes cargada")
    
    def show_points(self):
        """Mostrar gestión de puntos"""
        title = ctk.CTkLabel(
            self.main_frame,
            text="⭐ Puntos de Participación",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            self.main_frame,
            text="Aquí podrás asignar y gestionar puntos de participación",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info.pack(pady=10)
    
    def show_classes(self):
        """Mostrar gestión de clases"""
        title = ctk.CTkLabel(
            self.main_frame,
            text="📚 Mis Clases",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            self.main_frame,
            text="Aquí podrás gestionar tus clases y secciones",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info.pack(pady=10)
    
    def show_reports(self):
        """Mostrar reportes"""
        title = ctk.CTkLabel(
            self.main_frame,
            text="📈 Reportes",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            self.main_frame,
            text="Aquí podrás exportar reportes a Excel",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info.pack(pady=10)
    
    def show_settings(self):
        """Mostrar configuración"""
        title = ctk.CTkLabel(
            self.main_frame,
            text="⚙️ Configuración",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        info = ctk.CTkLabel(
            self.main_frame,
            text="Aquí podrás configurar tu cuenta y el sistema",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info.pack(pady=10)
    
    def manual_sync(self):
        """Realizar sincronización manual"""
        self.sync_button.configure(state="disabled", text="Sincronizando...")
        self.sync_status_label.configure(text="Sincronizando...", text_color="yellow")
        self.update()
        
        try:
            sync_manager.manual_sync(direction="bidireccional")
            self.sync_status_label.configure(
                text="✓ Sincronización exitosa",
                text_color="green"
            )
            logger.info("Sincronización manual completada")
        except Exception as e:
            self.sync_status_label.configure(
                text="✗ Error en sincronización",
                text_color="red"
            )
            logger.error(f"Error en sincronización manual: {e}")
        
        self.sync_button.configure(state="normal", text="🔄 Sincronizar Ahora")
    
    def logout(self):
        """Cerrar sesión"""
        logger.info(f"Cerrando sesión: {self.usuario.nombre}")
        sync_manager.stop_auto_sync()
        self.destroy()
        
        from src.ui.login_window import LoginWindow
        app = LoginWindow()
        app.mainloop()
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        logger.info("Cerrando aplicación...")
        sync_manager.stop_auto_sync()
        self.destroy()
