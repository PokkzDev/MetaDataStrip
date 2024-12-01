import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from image_processor import ImageProcessor

class MetadataStripperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata Stripper")
        self.file_paths = []

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

    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg='#34495e', fg='white')
        self.root.config(menu=menu_bar)

        app_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label="App", menu=app_menu)
        app_menu.add_command(label="Preferences", command=self.show_preferences)
        app_menu.add_separator()
        app_menu.add_command(label="Exit", command=self.close_app)

        resolution_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label="Resolution", menu=resolution_menu)
        resolutions = ["1280x720", "1366x768", "1600x900"]
        for res in resolutions:
            resolution_menu.add_command(label=res, command=lambda r=res: self.set_resolution(r))

        help_menu = tk.Menu(menu_bar, tearoff=0, bg='#34495e', fg='white')
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

    def create_widgets(self):
        self.metadata_display = tk.Text(self.root, height=20, width=80, bg='#ecf0f1', fg='black', font=('Helvetica', 10))
        self.metadata_display.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.button_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.button_frame.grid(row=1, column=0, pady=10, sticky=(tk.E, tk.S))

        select_button = ttk.Button(self.button_frame, text="Select Images", command=self.process_images)
        select_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        remove_button = ttk.Button(self.button_frame, text="Remove Metadata", command=self.remove_metadata_from_selected_images)
        remove_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

    def process_images(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.webp;*.heic")])
        if not self.file_paths:
            return

        self.metadata_display.delete(1.0, tk.END)
        for file_path in self.file_paths:
            try:
                metadata = ImageProcessor.display_metadata(file_path)
                self.metadata_display.insert(tk.END, f"Metadata for {file_path}:\n{metadata}\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {file_path}: {e}")
                self.metadata_display.insert(tk.END, f"Error processing {file_path}: {e}\n\n")

    def remove_metadata_from_selected_images(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No images selected.")
            return

        for file_path in self.file_paths:
            try:
                temp_path = ImageProcessor.remove_metadata(file_path)
                ImageProcessor.save_image(temp_path, file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {file_path}: {e}")
                return

        messagebox.showinfo("Success", "Metadata removed from selected images.")

    def set_resolution(self, resolution):
        width, height = map(int, resolution.split('x'))
        self.root.geometry(f"{width}x{height}")
        self.metadata_display.config(width=width // 10, height=height // 30)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.metadata_display.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.button_frame.grid(row=1, column=0, pady=10, sticky=(tk.E, tk.S))

    def show_about(self):
        about_text = (
            "Metadata Stripper\n"
            "Version 1.0\n\n"
            "Developed by Pokkz.dev\n"
            "Fullstack Web Developer\n"
            "2024\n\n"
            "For more information, visit:\n"
            "https://pokkz.dev"
        )
        messagebox.showinfo("About Metadata Stripper", about_text)

    def show_preferences(self):
        preferences_text = (
            "Preferences:\n\n"
            "1. Default Save Location: Same as original image\n"
            "2. Image Quality: High\n"
            "3. Metadata Removal: Complete\n\n"
            "These preferences can be customized in future versions."
        )
        messagebox.showinfo("Preferences", preferences_text)

    def show_help(self):
        help_text = (
            "How to Use Metadata Stripper:\n\n"
            "1. Click 'Select Images' to choose the images you want to process.\n"
            "2. Review the metadata displayed in the text area.\n"
            "3. Click 'Remove Metadata' to strip metadata from the selected images.\n"
            "4. The processed images will be saved in the same directory with '_NOMETADATA' appended to their filenames.\n\n"
            "For more information, visit: https://pokkz.dev"
        )
        messagebox.showinfo("Help", help_text)

    def close_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataStripperApp(root)
    root.mainloop()
