import tkinter as tk
from tkinter import filedialog, messagebox
import os


class TextEditor:
    def __init__(self, root, filename=None):
        self.root = root
        self.filename = filename
        self.modified = False
        
        # Настройка окна
        self.root.title("Text Editor - Untitled")
        self.root.geometry("800x600")
        
        # Создание меню
        self.create_menu()
        
        # Создание текстового поля с прокруткой
        self.create_text_area()
        
        # Статусная строка
        self.create_status_bar()
        
        # Загрузка файла, если указан
        if self.filename:
            self.load_file()
        
        # Привязка событий
        self.bind_events()
        
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Window", command=self.new_window, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Ctrl+Q")
        
        # Меню Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        
    def create_text_area(self):
        """Создание текстового поля"""
        # Фрейм для текстового поля и скроллбаров
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Вертикальный скроллбар
        v_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Горизонтальный скроллбар
        h_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Текстовое поле
        self.text_area = tk.Text(
            text_frame,
            wrap=tk.WORD,  # Перенос по словам
            undo=True,  # Включаем встроенный undo
            font=("Courier New", 12),
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Связываем скроллбары с текстовым полем
        v_scrollbar.config(command=self.text_area.yview)
        h_scrollbar.config(command=self.text_area.xview)
        
    def create_status_bar(self):
        """Создание статусной строки"""
        self.status_bar = tk.Label(
            self.root,
            text="Ln 1, Col 1",
            anchor=tk.W,
            relief=tk.SUNKEN,
            bd=1
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def bind_events(self):
        """Привязка событий"""
        # Горячие клавиши
        self.root.bind("<Control-n>", lambda e: self.new_window())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
        self.root.bind("<Control-x>", lambda e: self.cut())
        self.root.bind("<Control-c>", lambda e: self.copy())
        self.root.bind("<Control-v>", lambda e: self.paste())
        
        # Отслеживание изменений в тексте
        self.text_area.bind("<<Modified>>", self.on_text_modified)
        
        # Обновление статусной строки при движении курсора
        self.text_area.bind("<KeyRelease>", self.update_status)
        self.text_area.bind("<ButtonRelease-1>", self.update_status)
        
    def new_window(self):
        """Открытие нового окна для того же файла"""
        new_root = tk.Toplevel()
        TextEditor(new_root, self.filename)
        
    def open_file(self):
        """Открытие файла"""
        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.filename = filename
            self.load_file()
            
    def load_file(self):
        """Загрузка содержимого файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                # Заменяем \r\n на \n (Windows)
                content = content.replace('\r\n', '\n')
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.root.title(f"Text Editor - {os.path.basename(self.filename)}")
                self.modified = False
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            
    def save_file(self):
        """Сохранение файла"""
        if not self.filename:
            self.save_file_as()
        else:
            try:
                content = self.text_area.get(1.0, tk.END)
                # Убираем последний лишний \n, который tkinter добавляет
                content = content[:-1] if content.endswith('\n') else content
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.modified = False
                self.root.title(f"Text Editor - {os.path.basename(self.filename)}")
                self.status_bar.config(text=f"Saved: {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
                
    def save_file_as(self):
        """Сохранение файла как..."""
        filename = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.filename = filename
            self.save_file()
            
    def undo(self):
        """Отмена действия"""
        self.text_area.edit_undo()
            
    def redo(self):
        """Повтор действия"""
        self.text_area.edit_redo()
            
    def cut(self):
        """Вырезать"""
        self.text_area.event_generate("<<Cut>>")
        
    def copy(self):
        """Копировать"""
        self.text_area.event_generate("<<Copy>>")
        
    def paste(self):
        """Вставить"""
        start = self.text_area.index(tk.INSERT)
        self.text_area.event_generate("<<Paste>>")
        self.text_area.see(start)
        self.update_status()
        
    def on_text_modified(self, event=None):
        """Обработка изменения текста"""
        if self.text_area.edit_modified():
            self.modified = True
            if self.filename:
                title = f"Text Editor - {os.path.basename(self.filename)} *"
            else:
                title = "Text Editor - Untitled *"
            self.root.title(title)
            self.text_area.edit_modified(False)
            
    def update_status(self, event=None):
        """Обновление статусной строки"""
        cursor_pos = self.text_area.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.status_bar.config(text=f"Ln {line}, Col {int(col) + 1}")
        
    def exit_app(self):
        """Выход из приложения"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "Do you want to save changes before closing?"
            )
            if response is True:  # Yes
                self.save_file()
                self.root.destroy()
            elif response is False:  # No
                self.root.destroy()
            # Cancel - ничего не делаем
        else:
            self.root.destroy()


def main():
    import sys
    
    root = tk.Tk()
    
    # Если передан аргумент командной строки - открываем файл
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    
    editor = TextEditor(root, filename)
    root.mainloop()


if __name__ == "__main__":
    main()