import tkinter as tk
from .logs import Logger
from .config import ShellConfig

class ShellEmulatorGUI:
    def __init__(self, root, virtual_fs, config_path):
        self.root = root
        self.root.title("Эмулятор Shell")
        self.virtual_fs = virtual_fs
        
        # Создание виджетов для отображения текста
        self.text_area = tk.Text(root, height=20, width=80, bg="black", fg="white", font=("Courier", 12))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.entry = tk.Entry(root, width=80, font=("Courier", 12))
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)
      
        self.text_area.tag_configure("green", foreground="lime")
        self.text_area.tag_configure("folder", foreground="#b3dcfd")
        self.text_area.tag_configure("file", foreground="white")

        self.config = ShellConfig(config_path)
        self.logger = Logger(self.config.path_to_log_file, self.config.username)

        self.text_area.insert(tk.END, f"{self.virtual_fs.current_dir}  \n", "green")
        self.text_area.insert(tk.END, f"{self.config.username} ❯ ")
        self.text_area.config(state=tk.DISABLED)  # Отключаем редактирование text_area


    def execute_command(self, event):
        self.text_area.config(state=tk.NORMAL)

        command = self.entry.get()

        self.text_area.insert(tk.END, f"{command}\n")
        output = self.process_command(command)
        if output:
            self.text_area.insert(tk.END, f"{output}\n")
        self.text_area.insert(tk.END, f"\n{self.virtual_fs.current_dir}  \n", "green")
        self.text_area.insert(tk.END, f"{self.config.username} ❯ ")

        # Отключаем редактирование после записи
        self.text_area.config(state=tk.DISABLED)
        
        # Очищаем командную строку
        self.entry.delete(0, tk.END)

    def process_command(self, command):
        # Разделяем команду на составляющие
        parts = command.split()
        cmd = parts[0]

        # Используем match-case для обработки команд
        match cmd:
            case "ls":
                return self.command_ls()
            case "cat":
                return self.command_cat(parts)
            case "who":
                return self.command_who()
            case "cd":
                return self.command_cd(parts)
            case "find":
                return self.command_find(parts)
            case "exit":
                self.root.quit()
            case "wc":
                return self.command_wc(parts)
            case _:
                return "Команда не поддерживается."
    # Метод для команды ls
    def command_ls(self):
        contents = self.virtual_fs.list_dir()
        output = ""
        
        for item in contents:
            if item.endswith('/'):  # Если элемент — папка
                self.text_area.insert(tk.END, f"{item}\n", "folder")
            else:  # Если элемент — файл
                self.text_area.insert(tk.END, f"{item}\n", "file")
                
        return output
    
    # Метод для команды cat
    def command_cat(self, parts):
        if len(parts) < 2:
            return "Ошибка: не указан файл."
        try:
            file_content = self.virtual_fs.read_file(parts[1])
            return file_content
        except KeyError:
            return "Ошибка: файл не найден."

    # Метод для команды who
    def command_who(self):
        return f"Current user: {self.config.username}"

    # Метод для команды cd
    def command_cd(self, parts):
        if len(parts) < 2:
            return "Ошибка: не указана директория."
        
        target_dir = parts[1]
        self.virtual_fs.change_dir(target_dir)
        return ""

    # Метод для команды exit
    def command_exit(self):
        self.root.quit()

    def command_find(self, parts):
        if len(parts) < 2:
            return "Ошибка: укажите имя для поиска."

        search_name = parts[1]
        matching_files = self.virtual_fs.find(search_name)
        
        if not matching_files:
            return f"Нет совпадений для '{search_name}'."
        
        # Возвращаем результаты поиска как строки
        return "\n".join(matching_files)

    def command_wc(self, parts):
        if len(parts) < 2:
            return "Ошибка: укажите файл для команды wc."

        file_path = parts[1]
        result = self.virtual_fs.wc(file_path)

        if isinstance(result, str):
            # Если результат — строка, значит, произошла ошибка
            return result
        else:
            num_lines, num_words, num_chars = result
            return f"Строк: {num_lines}, Слов: {num_words}, Символов: {num_chars}"
