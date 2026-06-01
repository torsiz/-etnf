import customtkinter as ctk
from tkinter import filedialog, messagebox, Text, Menu
import os
import sys
import subprocess
import webbrowser

class NotepadApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Notepad IDE")
        self.geometry("1000x700")
        self.current_file_path = None
        
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text_editor = Text(
            self,
            wrap="word", undo=True, bg="#2B2B2B", fg="white",
            insertbackground="white", selectbackground="#4a4a4a",
            font=("Consolas", 14), borderwidth=0, highlightthickness=0
        )
        self.text_editor.grid(row=0, column=0, sticky="nsew")
        
        self.output_console_frame = ctk.CTkFrame(self, height=150)
        self.output_console_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.output_console_frame.grid_rowconfigure(0, weight=1)
        self.output_console_frame.grid_columnconfigure(0, weight=1)
        
        self.output_console = ctk.CTkTextbox(
            self.output_console_frame,
            font=("Consolas", 12),
            wrap="word",
            activate_scrollbars=True
        )
        self.output_console.grid(row=0, column=0, sticky="nsew")
        self.output_console_frame.grid_remove() 
        self.is_console_visible = False

        self.create_menu_bar()
        
        self.text_editor.bind("<KeyRelease>", self.update_status)
        self.text_editor.bind("<ButtonRelease>", self.update_status)
        
        self.status_bar = ctk.CTkLabel(self, text="Строка: 1, Столбец: 0", height=20, anchor="w")
        self.grid_rowconfigure(2, weight=0) 
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10)

    def toggle_console(self):
        if self.is_console_visible:
            self.output_console_frame.grid_remove()
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)
            self.is_console_visible = False
        else:
            self.output_console_frame.grid()
            self.grid_rowconfigure(0, weight=4)
            self.grid_rowconfigure(1, weight=1)
            self.is_console_visible = True
            
    def run_code(self):
        if self.current_file_path is None:
            if not self.save_as_file():
                messagebox.showwarning("Отмена", "Файл не был сохранен. Запуск отменен.")
                return
        else:
            self.save_file()

        if not self.is_console_visible:
            self.toggle_console()
        self.output_console.delete("1.0", "end")

        file_extension = os.path.splitext(self.current_file_path)[1]
        
        if file_extension == ".py":
            self.output_console.insert("end", f"--- Запуск {os.path.basename(self.current_file_path)} ---\n\n")
            command = [sys.executable, self.current_file_path]
            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, check=True, encoding='utf-8',
                    cwd=os.path.dirname(self.current_file_path)
                )
                self.output_console.insert("end", result.stdout)
                if result.stderr:
                    self.output_console.insert("end", f"\n--- Ошибки ---\n{result.stderr}", "error")
            except subprocess.CalledProcessError as e:
                self.output_console.insert("end", e.stdout, "output")
                self.output_console.insert("end", e.stderr, "error")
            except FileNotFoundError:
                self.output_console.insert("end", "Ошибка: Интерпретатор Python не найден.", "error")
            self.output_console.insert("end", "\n\n--- Выполнение завершено ---")

        elif file_extension in [".html", ".css", ".js"]:
            self.output_console.insert("end", f"Открытие {os.path.basename(self.current_file_path)} в браузере...")
            
            file_to_open = self.current_file_path
            
            if file_extension in [".css", ".js"]:
                temp_html_path = self._create_temp_runner(self.current_file_path, file_extension)
                if temp_html_path:
                    file_to_open = temp_html_path
                else:
                    self.output_console.insert("end", "\nНе удалось создать временный файл.", "error")
                    return

            webbrowser.open('file://' + os.path.realpath(file_to_open))
            self.output_console.insert("end", " Готово!")

        else:
            self.output_console.insert("end", f"Невозможно запустить файлы типа '{file_extension}'.", "error")

        self.output_console.tag_config("error", foreground="#FF5555")
        self.output_console.tag_config("output", foreground="white")

    def _create_temp_runner(self, file_path, extension):
        filename = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)
        temp_html_path = os.path.join(dir_path, "_runner_temp.html")

        html_content = ""
        if extension == ".css":
            html_content = f"""
            <!DOCTYPE html><html><head>
            <link rel="stylesheet" href="{filename}">
            <title>CSS Test</title></head><body>
            <h1>Это тестовая страница для {filename}</h1>
            <p>Этот параграф и заголовок должны быть стилизованы вашим CSS.</p>
            </body></html>"""
        elif extension == ".js":
            html_content = f"""
            <!DOCTYPE html><html><head><title>JS Test</title></head><body>
            <h1>Тестовая страница для {filename}</h1>
            <p>Проверьте консоль разработчика (F12) для вывода вашего скрипта.</p>
            <script src="{filename}"></script>
            </body></html>"""
        
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            return temp_html_path
        except IOError:
            return None

    def create_menu_bar(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)
        
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        run_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Запуск", menu=run_menu)
        run_menu.add_command(label="Запустить код", accelerator="F5", command=self.run_code)
        run_menu.add_command(label="Показать/скрыть консоль", command=self.toggle_console)
        self.bind("<F5>", lambda event: self.run_code()) # Горячая клавиша F5

        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit_application)
        
        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Правка", menu=edit_menu)
    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Все файлы", "*.*")])
        if not filepath: return False
        try:
            with open(filepath, "w", encoding="utf-8") as file: file.write(self.text_editor.get(1.0, "end-1c"))
            self.current_file_path = filepath
            self.title(f"{os.path.basename(filepath)} - Notepad IDE")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка!", f"Не удалось сохранить файл:\n{e}")
            return False
    
    def update_status(self, event=None):
        row, col = self.text_editor.index("insert").split('.')
        self.status_bar.configure(text=f"Строка: {row}, Столбец: {col}")
    def new_file(self):
        self.current_file_path = None
        self.text_editor.delete("1.0", "end")
        self.title("Новый файл - Notepad IDE")
        self.update_status()
    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt"),("Python", "*.py"),("HTML", "*.html"),("JavaScript", "*.js"),("CSS", "*.css"), ("Все файлы", "*.*")])
        if not filepath: return
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("end", file.read())
            self.current_file_path = filepath
            self.title(f"{os.path.basename(filepath)} - Notepad IDE")
            self.update_status()
        except Exception as e: messagebox.showerror("Ошибка", f"Произошла ошибка при открытии файла: {e}")
    def save_file(self):
        if self.current_file_path is None: self.save_as_file()
        else:
            try:
                with open(self.current_file_path, "w", encoding="utf-8") as file: file.write(self.text_editor.get(1.0, "end-1c"))
                self.title(f"{os.path.basename(self.current_file_path)} - Notepad IDE")
            except Exception as e: messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении файла: {e}")
    def quit_application(self): self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = NotepadApp()
    app.mainloop()