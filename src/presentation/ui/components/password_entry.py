"""
Componente PasswordEntry reutilizable
Entry personalizado para contraseñas con botón mostrar/ocultar
CORRIGE BUG: Letras no se ven en registro
"""
import customtkinter as ctk


class PasswordEntry(ctk.CTkFrame):
    """Entry personalizado para contraseña con botón mostrar/ocultar integrado"""
    
    def __init__(self, parent, placeholder_text="Contraseña", width=400, height=40, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.password_visible = False
        self.width = width
        self.height = height
        
        # Frame que simula un input (con borde)
        self.entry_frame = ctk.CTkFrame(
            self,
            fg_color=("#F9F9FA", "#343638"),
            border_color=("#979DA2", "#565B5E"),
            border_width=2,
            corner_radius=8,
            width=width,
            height=height
        )
        self.entry_frame.pack(fill="both", expand=True)
        self.entry_frame.pack_propagate(False)
        
        # Entry sin borde (dentro del frame)
        # 🔥 FIX: text_color para que las letras se vean
        self.entry = ctk.CTkEntry(
            self.entry_frame,
            placeholder_text=placeholder_text,
            show="*",
            width=width-50,
            height=height,
            border_width=0,
            fg_color="transparent",
            font=ctk.CTkFont(size=14),
            text_color=("gray10", "gray90")  # ← FIX: Texto visible en ambos modos
        )
        self.entry.place(x=8, y=0)
        
        # Botón mostrar/ocultar (centrado verticalmente)
        self.toggle_btn = ctk.CTkButton(
            self.entry_frame,
            text="👁️",
            width=40,
            height=height,
            command=self.toggle_visibility,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            corner_radius=6,
            font=ctk.CTkFont(size=18)
        )
        self.toggle_btn.place(x=width-45, y=0)
    
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
    
    def delete(self, start, end='end'):
        """Borrar texto"""
        self.entry.delete(start, end)
    
    def insert(self, index, text):
        """Insertar texto"""
        self.entry.insert(index, text)
    
    def focus(self):
        """Dar foco al entry"""
        self.entry.focus()
    
    def bind(self, *args, **kwargs):
        """Pasar bind al entry interno"""
        return self.entry.bind(*args, **kwargs)
    
    def configure(self, **kwargs):
        """Configurar el entry"""
        if 'state' in kwargs:
            self.entry.configure(state=kwargs.pop('state'))
        super().configure(**kwargs)
