import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from image_processor import ImageProcessor  # Import ImageProcessor

class MetadataStripperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MetaStripper")
        self.file_paths = []
        self.language = 'en'  # Default language

        # Text for both languages
        self.texts = {
            'en': {
                'title': "MetaStripper",
                'preferences': "Preferences",
                'exit': "Exit",
                'resolution': "Resolution",
                'help': "Help",
                'about': "About",
                'filename': "Filename",
                'has_metadata': "Has Metadata",
                'options': "Options",
                'add_images': "Add Images",
                'add_folder': "Add Folder",
                'remove_metadata': "Remove Metadata",
                'remove_all_images': "Remove All Images",
                'success': "Success",
                'metadata_removed': "Metadata removed from selected images.",
                'error': "Error",
                'no_images_selected': "No images selected.",
                'no_images_to_remove': "No images to remove.",
                'about_text': (
                    "MetaStripper\n"
                    "Version 1.0\n\n"
                    "Developed by Pokkz.dev\n"
                    "Fullstack Web Developer\n"
                    "2024\n\n"
                    "For more information, visit:\n"
                    "https://pokkz.dev"
                ),
                'preferences_text': (
                    "Preferences:\n\n"
                    "1. Default Save Location: Same as original image\n"
                    "2. Image Quality: High\n"
                    "3. Metadata Removal: Complete\n\n"
                    "These preferences can be customized in future versions."
                ),
                'help_text': (
                    "How to Use MetaStripper:\n\n"
                    "1. Click 'Add Images' to choose the images you want to process.\n"
                    "2. Review the metadata displayed in the table.\n"
                    "3. Click 'Remove Metadata' to strip metadata from the selected images.\n"
                    "4. The processed images will be saved in the same directory.\n\n"
                    "For more information, visit: https://pokkz.dev"
                )
            },
            'es': {
                'title': "MetaStripper",
                'preferences': "Preferencias",
                'exit': "Salir",
                'resolution': "Resolución",
                'help': "Ayuda",
                'about': "Acerca de",
                'filename': "Nombre de Archivo",
                'has_metadata': "Tiene Metadatos",
                'options': "Opciones",
                'add_images': "Agregar Imágenes",
                'add_folder': "Agregar Carpeta",
                'remove_metadata': "Eliminar Metadatos",
                'remove_all_images': "Eliminar Todas las Imágenes",
                'success': "Éxito",
                'metadata_removed': "Metadatos eliminados de las imágenes seleccionadas.",
                'error': "Error",
                'no_images_selected': "No se seleccionaron imágenes.",
                'no_images_to_remove': "No hay imágenes para eliminar.",
                'about_text': (
                    "MetaStripper\n"
                    "Versión 1.0\n\n"
                    "Desarrollado por Pokkz.dev\n"
                    "Desarrollador Web Fullstack\n"
                    "2024\n\n"
                    "Para más información, visite:\n"
                    "https://pokkz.dev"
                ),
                'preferences_text': (
                    "Preferencias:\n\n"
                    "1. Ubicación de Guardado Predeterminada: Igual que la imagen original\n"
                    "2. Calidad de Imagen: Alta\n"
                    "3. Eliminación de Metadatos: Completa\n\n"
                    "Estas preferencias se pueden personalizar en futuras versiones."
                ),
                'help_text': (
                    "Cómo Usar MetaStripper:\n\n"
                    "1. Haga clic en 'Agregar Imágenes' para elegir las imágenes que desea procesar.\n"
                    "2. Revise los metadatos mostrados en la tabla.\n"
                    "3. Haga clic en 'Eliminar Metadatos' para eliminar los metadatos de las imágenes seleccionadas.\n"
                    "4. Las imágenes procesadas se guardarán en el mismo directorio.\n\n"
                    "Para más información, visite: https://pokkz.dev"
                )
            }
        }

        # Apply custom styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2c3e50')
        style.configure('TButton', background='#3498db', foreground='white', font=('Helvetica', 10, 'bold'))
        style.map('TButton', background=[('active', '#2980b9')])
        style.configure('TLabel', background='#2c3e50', foreground='white', font=('Helvetica', 10))
        style.configure('TText', background='#ecf0f1', foreground='black', font=('Helvetica', 10))

        self.root.configure(bg='#2c3e50')

        self.create_menu()
        self.create_widgets()

        # Set initial resolution
        self.set_resolution("1024x576")

    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg='#34495e', fg='white')
        self.root.config(menu=menu_bar)

        app_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label=self.texts[self.language]['preferences'], menu=app_menu)
        app_menu.add_command(label=self.texts[self.language]['preferences'], command=self.show_preferences)
        app_menu.add_separator()
        app_menu.add_command(label=self.texts[self.language]['exit'], command=self.close_app)

        resolution_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label=self.texts[self.language]['resolution'], menu=resolution_menu)
        resolutions = ["1024x576", "1280x720", "1920x1080"]
        for res in resolutions:
            resolution_menu.add_command(label=res, command=lambda r=res: self.set_resolution(r))

        help_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label=self.texts[self.language]['help'], menu=help_menu)
        help_menu.add_command(label=self.texts[self.language]['help'], command=self.show_help)
        help_menu.add_command(label=self.texts[self.language]['about'], command=self.show_about)

        language_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label="Language", menu=language_menu)
        language_menu.add_command(label="English", command=lambda: self.set_language('en'))
        language_menu.add_command(label="Español", command=lambda: self.set_language('es'))

    def set_language(self, language):
        self.language = language
        self.root.title(self.texts[self.language]['title'])
        self.create_menu()
        self.create_widgets()  # Update widgets to reflect the new language
        self.refresh_metadata_display()

    def create_widgets(self):
        self.metadata_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.metadata_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Add titles
        ttk.Label(self.metadata_frame, text=self.texts[self.language]['filename'], font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Label(self.metadata_frame, text=self.texts[self.language]['has_metadata'], font=('Helvetica', 10, 'bold')).grid(
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        ttk.Label(self.metadata_frame, text=self.texts[self.language]['options'], font=('Helvetica', 10, 'bold')).grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )

        self.metadata_frame.grid_columnconfigure(0, weight=3)  # Filename column
        self.metadata_frame.grid_columnconfigure(1, weight=1)  # Metadata column
        self.metadata_frame.grid_columnconfigure(2, weight=1)  # Options column

        # Add a canvas and scrollbar for the metadata frame
        self.canvas = tk.Canvas(self.metadata_frame, bg='#2c3e50', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.metadata_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Store the window ID
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the canvas configure event
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.scrollbar.grid(row=1, column=3, sticky="ns")

        self.metadata_frame.grid_rowconfigure(1, weight=1)  # Ensure canvas row expands
        self.scrollable_frame.grid_columnconfigure(0, weight=3)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        self.button_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.button_frame.grid(row=2, column=0, pady=10, sticky=(tk.E, tk.S))

        remove_all_button = ttk.Button(self.button_frame, text=self.texts[self.language]['remove_all_images'], command=self.remove_all_images)
        remove_all_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        add_images_button = ttk.Button(self.button_frame, text=self.texts[self.language]['add_images'], command=self.add_images)
        add_images_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        add_folder_button = ttk.Button(self.button_frame, text=self.texts[self.language]['add_folder'], command=self.add_folder)
        add_folder_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

        remove_button = ttk.Button(self.button_frame, text=self.texts[self.language]['remove_metadata'], command=self.remove_metadata_from_selected_images)
        remove_button.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=0)
        self.button_frame.grid_columnconfigure(3, weight=0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)

        # Bind mouse wheel to the canvas for scrolling
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)

    def on_canvas_configure(self, event):
        # Update the scrollable_frame's width to fill the canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp;*.heic")])
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.file_paths:
                    self.file_paths.append(file_path)
            self.refresh_metadata_display()

    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp', '.heic')):
                        file_path = os.path.join(root, file)
                        if file_path not in self.file_paths:
                            self.file_paths.append(file_path)
            self.refresh_metadata_display()

    def refresh_metadata_display(self):
        # Clear current displayed data
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Re-draw all file entries with aligned columns
        for index, file_path in enumerate(self.file_paths):
            self.display_metadata(file_path, index)

    def display_metadata(self, file_path, row):
        try:
            has_metadata = "Yes" if ImageProcessor.has_metadata(file_path) else "No"  # Use ImageProcessor
            ttk.Label(self.scrollable_frame, text=os.path.basename(file_path), anchor="w").grid(
                row=row, column=0, padx=5, pady=5, sticky="nsew"
            )
            ttk.Label(self.scrollable_frame, text=has_metadata, anchor="center").grid(
                row=row, column=1, padx=5, pady=5, sticky="nsew"
            )
            remove_button = ttk.Button(
                self.scrollable_frame, text=self.texts[self.language]['remove_metadata'], command=lambda r=row, fp=file_path: self.remove_image(r, fp)
            )
            remove_button.grid(row=row, column=2, padx=5, pady=5, sticky="nsew")
        except Exception as e:
            messagebox.showerror(self.texts[self.language]['error'], f"Failed to process {file_path}: {e}")

    def remove_image(self, row, file_path):
        if file_path in self.file_paths:
            self.file_paths.remove(file_path)
            self.refresh_metadata_display()

    def remove_metadata_from_selected_images(self):
        if not self.file_paths:
            messagebox.showerror(self.texts[self.language]['error'], self.texts[self.language]['no_images_selected'])
            return

        for file_path in self.file_paths:
            try:
                temp_path = ImageProcessor.remove_metadata(file_path)  # Use ImageProcessor
                ImageProcessor.save_image(temp_path, file_path)        # Use ImageProcessor
            except Exception as e:
                messagebox.showerror(self.texts[self.language]['error'], f"Failed to process {file_path}: {e}")
                return

        messagebox.showinfo(self.texts[self.language]['success'], self.texts[self.language]['metadata_removed'])

    def remove_all_images(self):
        if self.file_paths:
            self.file_paths.clear()
            self.refresh_metadata_display()
        else:
            messagebox.showerror(self.texts[self.language]['error'], self.texts[self.language]['no_images_to_remove'])

    def set_resolution(self, resolution):
        width, height = map(int, resolution.split('x'))
        self.root.geometry(f"{width}x{height}")

    def show_about(self):
        messagebox.showinfo(self.texts[self.language]['about'], self.texts[self.language]['about_text'])

    def show_preferences(self):
        messagebox.showinfo(self.texts[self.language]['preferences'], self.texts[self.language]['preferences_text'])

    def show_help(self):
        messagebox.showinfo(self.texts[self.language]['help'], self.texts[self.language]['help_text'])

    def close_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataStripperApp(root)
    root.mainloop()
