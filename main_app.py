import customtkinter as ctk
from tkinter import filedialog, messagebox, Text, Menu
import os

class NotepadApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Notepad")
        self.geometry("900x600")
        self.current_file_path = None
        
        self.text_editor = Text(
            self,
            wrap="word",
            undo=True,
            bg="#2B2B2B",
            fg="white",
            insertbackground="white",
            selectbackground="#4a4a4a",
            font=("Consolas", 12)
        )
        self.text_editor.pack(expand=True, fill="both")
        
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)
        
        # --- Меню "Файл" ---
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit_application)

        # --- Меню "Правка" ---
        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self.text_editor.edit_undo)
        edit_menu.add_command(label="Вернуть", command=self.text_editor.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", accelerator="Ctrl+X", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копировать", accelerator="Ctrl+C", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставить", accelerator="Ctrl+V", command=lambda: self.text_editor.event_generate("<<Paste>>"))
        
    def new_file(self):
        self.current_file_path = None
        self.text_editor.delete("1.0", "end")
        self.title("Новый файл - Notepad")
        
    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return
        
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_editor.delete("1.0", "end")
                self.text_editor.insert("end", content)
            self.current_file_path = filepath
            self.title(f"{os.path.basename(filepath)} - Notepad")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при открытии файла: {e}")
            
    def save_file(self):
        if self.current_file_path is None:
            self.save_as_file()
        else:
            try:
                content = self.text_editor.get(1.0, "end-1c")
                with open(self.current_file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.title(f"{os.path.basename(self.current_file_path)} - Notepad")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при сохранении файла: {e}")
                
    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return

        try:
            content = self.text_editor.get(1.0, "end-1c")
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            self.current_file_path = filepath
            self.title(f"{os.path.basename(filepath)} - Блокнот")
        except Exception as e:
            messagebox.showerror("Ошибка!", f"Не удалось сохранить файл:\n{e}")
            
    def quit_application(self):
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = NotepadApp()
    app.mainloop()
