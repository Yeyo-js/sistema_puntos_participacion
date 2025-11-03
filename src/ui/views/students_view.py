"""
Vista de Gestión de Estudiantes
Interfaz completa para el CRUD de estudiantes
"""
import customtkinter as ctk
from src.controllers.student_controller import StudentController
from src.config.settings import COLORS
import logging

logger = logging.getLogger(__name__)

class StudentsView(ctk.CTkFrame):
    """Vista principal de gestión de estudiantes"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="gray95")
        
        self.controller = StudentController()
        self.selected_student_id = None
        
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        """Crear todos los widgets de la vista"""
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="👥 Gestión de Estudiantes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["primary"]
        )
        title.pack(side="left")
        
        # Barra de acciones
        actions_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        actions_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Búsqueda
        search_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        search_frame.pack(side="left", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar estudiante...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_students())
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=100,
            height=35,
            command=self.search_students,
            fg_color=COLORS["info"]
        )
        search_btn.pack(side="left")
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10, pady=10)
        
        self.btn_add = ctk.CTkButton(
            buttons_frame,
            text="➕ Agregar Estudiante",
            width=150,
            height=35,
            command=self.show_add_dialog,
            fg_color=COLORS["success"]
        )
        self.btn_add.pack(side="left", padx=5)
        
        self.btn_edit = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            width=120,
            height=35,
            command=self.show_edit_dialog,
            fg_color=COLORS["warning"],
            state="disabled"
        )
        self.btn_edit.pack(side="left", padx=5)
        
        self.btn_delete = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Eliminar",
            width=120,
            height=35,
            command=self.delete_student,
            fg_color=COLORS["danger"],
            state="disabled"
        )
        self.btn_delete.pack(side="left", padx=5)
        
        # Tabla de estudiantes
        table_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Headers de la tabla
        headers_frame = ctk.CTkFrame(table_frame, fg_color=COLORS["primary"], corner_radius=8)
        headers_frame.pack(fill="x", padx=10, pady=10)
        
        headers = ["N°", "Nombre Completo", "Sección", "Acciones"]
        widths = [80, 400, 200, 150]
        
        for header, width in zip(headers, widths):
            lbl = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white",
                width=width
            )
            lbl.pack(side="left", padx=5, pady=10)
        
        # Scrollable frame para estudiantes
        self.students_scroll = ctk.CTkScrollableFrame(
            table_frame,
            fg_color="transparent",
            height=400
        )
        self.students_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Información inferior
        self.info_label = ctk.CTkLabel(
            self,
            text="Total de estudiantes: 0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.info_label.pack(pady=(0, 10))
    
    def load_students(self):
        """Cargar y mostrar todos los estudiantes"""
        # Limpiar tabla
        for widget in self.students_scroll.winfo_children():
            widget.destroy()
        
        # Obtener estudiantes
        students = self.controller.get_all_students()
        
        if not students:
            # Mensaje si no hay estudiantes
            no_data_label = ctk.CTkLabel(
                self.students_scroll,
                text="📋 No hay estudiantes registrados\nHaz clic en 'Agregar Estudiante' para comenzar",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data_label.pack(pady=50)
        else:
            # Mostrar estudiantes
            for student in students:
                self.create_student_row(student)
        
        # Actualizar contador
        self.info_label.configure(text=f"Total de estudiantes: {len(students)}")
        
        logger.info(f"Tabla de estudiantes cargada: {len(students)} registros")
    
    def create_student_row(self, student):
        """Crear una fila en la tabla para un estudiante"""
        
        row_frame = ctk.CTkFrame(
            self.students_scroll,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="gray85"
        )
        row_frame.pack(fill="x", pady=5)
        
        # Número de lista
        num_label = ctk.CTkLabel(
            row_frame,
            text=str(student['list_number']),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=80,
            text_color=COLORS["primary"]
        )
        num_label.pack(side="left", padx=5, pady=10)
        
        # Nombre
        name_label = ctk.CTkLabel(
            row_frame,
            text=student['full_name'],
            font=ctk.CTkFont(size=13),
            width=400,
            anchor="w"
        )
        name_label.pack(side="left", padx=5, pady=10)
        
        # Sección
        section_label = ctk.CTkLabel(
            row_frame,
            text=student['section_name'],
            font=ctk.CTkFont(size=12),
            width=200,
            text_color="gray50"
        )
        section_label.pack(side="left", padx=5, pady=10)
        
        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=150)
        actions_frame.pack(side="left", padx=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=40,
            height=30,
            command=lambda s=student: self.edit_student(s),
            fg_color=COLORS["warning"],
            hover_color=COLORS["warning"]
        )
        edit_btn.pack(side="left", padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=40,
            height=30,
            command=lambda s=student: self.confirm_delete(s),
            fg_color=COLORS["danger"],
            hover_color="darkred"
        )
        delete_btn.pack(side="left", padx=2)
    
    def search_students(self):
        """Buscar estudiantes"""
        search_term = self.search_entry.get().strip()
        
        # Limpiar tabla
        for widget in self.students_scroll.winfo_children():
            widget.destroy()
        
        if not search_term:
            # Si no hay término de búsqueda, mostrar todos
            self.load_students()
            return
        
        # Buscar
        students = self.controller.search_students(search_term)
        
        if not students:
            no_results = ctk.CTkLabel(
                self.students_scroll,
                text=f"🔍 No se encontraron resultados para '{search_term}'",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_results.pack(pady=50)
        else:
            for student in students:
                self.create_student_row(student)
        
        self.info_label.configure(text=f"Resultados encontrados: {len(students)}")
    
    def show_add_dialog(self):
        """Mostrar diálogo para agregar estudiante"""
        dialog = StudentFormDialog(self, mode="add", controller=self.controller)
        dialog.grab_set()
        self.wait_window(dialog)
        
        if dialog.success:
            self.load_students()
    
    def show_edit_dialog(self):
        """Mostrar diálogo para editar estudiante"""
        if not self.selected_student_id:
            return
        
        student = self.controller.get_student_by_id(self.selected_student_id)
        if student:
            dialog = StudentFormDialog(
                self,
                mode="edit",
                controller=self.controller,
                student_data=student
            )
            dialog.grab_set()
            self.wait_window(dialog)
            
            if dialog.success:
                self.load_students()
    
    def edit_student(self, student):
        """Editar un estudiante"""
        dialog = StudentFormDialog(
            self,
            mode="edit",
            controller=self.controller,
            student_data=student
        )
        dialog.grab_set()
        self.wait_window(dialog)
        
        if dialog.success:
            self.load_students()
    
    def confirm_delete(self, student):
        """Confirmar eliminación de estudiante"""
        dialog = ConfirmDialog(
            self,
            title="Confirmar Eliminación",
            message=f"¿Estás seguro de eliminar al estudiante:\n\n{student['full_name']}?\n\nEsta acción no se puede deshacer."
        )
        dialog.grab_set()
        self.wait_window(dialog)
        
        if dialog.confirmed:
            result = self.controller.delete_student(student['id'])
            
            if result['success']:
                self.show_message("Estudiante eliminado exitosamente", "success")
                self.load_students()
            else:
                self.show_message(result['message'], "error")
    
    def delete_student(self):
        """Eliminar estudiante seleccionado"""
        if not self.selected_student_id:
            return
        
        student = self.controller.get_student_by_id(self.selected_student_id)
        if student:
            self.confirm_delete(student)
    
    def show_message(self, message, msg_type="info"):
        """Mostrar mensaje temporal"""
        color = COLORS["success"] if msg_type == "success" else COLORS["danger"]
        
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=13),
            text_color=color
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # Ocultar después de 3 segundos
        self.after(3000, msg_label.destroy)


class StudentFormDialog(ctk.CTkToplevel):
    """Diálogo para agregar/editar estudiante"""
    
    def __init__(self, parent, mode="add", controller=None, student_data=None):
        super().__init__(parent)
        
        self.controller = controller
        self.mode = mode
        self.student_data = student_data
        self.success = False
        
        # Configuración
        self.title("Agregar Estudiante" if mode == "add" else "Editar Estudiante")
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.create_widgets()
        
        if mode == "edit" and student_data:
            self.load_student_data()
        
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
        """Crear widgets del formulario"""
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="➕ Nuevo Estudiante" if self.mode == "add" else "✏️ Editar Estudiante",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["primary"]
        )
        title.pack(pady=(0, 20))
        
        # Número de lista
        ctk.CTkLabel(
            main_frame,
            text="Número de Lista:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        self.list_number_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ej: 1, 2, 3...",
            height=40
        )
        self.list_number_entry.pack(fill="x", pady=(0, 15))
        
        # Nombre completo
        ctk.CTkLabel(
            main_frame,
            text="Nombre Completo:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Ej: Juan Pérez García",
            height=40
        )
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        # Mensaje de error
        self.error_label = ctk.CTkLabel(
            main_frame,
            text="",
            text_color=COLORS["danger"],
            font=ctk.CTkFont(size=12)
        )
        self.error_label.pack(pady=(10, 10))
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=200,
            height=40,
            command=self.destroy,
            fg_color="gray",
            hover_color="gray30"
        )
        cancel_btn.pack(side="left", expand=True, padx=5)
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Guardar" if self.mode == "add" else "Actualizar",
            width=200,
            height=40,
            command=self.save_student,
            fg_color=COLORS["success"] if self.mode == "add" else COLORS["warning"]
        )
        save_btn.pack(side="right", expand=True, padx=5)
        
        # Focus en primer campo
        self.list_number_entry.focus()
    
    def load_student_data(self):
        """Cargar datos del estudiante en modo edición"""
        if self.student_data:
            self.list_number_entry.insert(0, str(self.student_data['list_number']))
            self.name_entry.insert(0, self.student_data['full_name'])
    
    def save_student(self):
        """Guardar estudiante"""
        # Validar campos
        list_number = self.list_number_entry.get().strip()
        full_name = self.name_entry.get().strip()
        
        if not list_number or not full_name:
            self.error_label.configure(text="⚠️ Todos los campos son obligatorios")
            return
        
        try:
            list_number = int(list_number)
        except ValueError:
            self.error_label.configure(text="⚠️ El número de lista debe ser un número")
            return
        
        if list_number < 1:
            self.error_label.configure(text="⚠️ El número de lista debe ser mayor a 0")
            return
        
        # Crear o actualizar sección de ejemplo si no existe
        section_id = self.controller.create_sample_section()
        
        # Guardar
        if self.mode == "add":
            result = self.controller.create_student(full_name, list_number, section_id)
        else:
            result = self.controller.update_student(
                self.student_data['id'],
                full_name=full_name,
                list_number=list_number
            )
        
        if result['success']:
            self.success = True
            self.destroy()
        else:
            self.error_label.configure(text=f"⚠️ {result['message']}")


class ConfirmDialog(ctk.CTkToplevel):
    """Diálogo de confirmación"""
    
    def __init__(self, parent, title="Confirmar", message="¿Estás seguro?"):
        super().__init__(parent)
        
        self.confirmed = False
        
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        
        # Mensaje
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        )
        msg_label.pack(pady=30, padx=20)
        
        # Botones
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            width=150,
            height=40,
            command=self.destroy,
            fg_color="gray"
        )
        cancel_btn.pack(side="left", padx=10)
        
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Confirmar",
            width=150,
            height=40,
            command=self.confirm,
            fg_color=COLORS["danger"]
        )
        confirm_btn.pack(side="right", padx=10)
        
        self.center_window()
    
    def center_window(self):
        """Centrar ventana"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def confirm(self):
        """Confirmar acción"""
        self.confirmed = True
        self.destroy()
