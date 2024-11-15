import zipfile
import os

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_file = zipfile.ZipFile(zip_path, 'r')
        # Устанавливаем текущую директорию в корень архива
        self.current_dir = zip_path.split(".")[1].strip("/") + "/"

    def list_dir(self):
        contents = []
        for info in self.zip_file.infolist():
            # Проверяем, является ли запись папкой (заканчивается на '/')
            if info.filename.startswith(self.current_dir):
                relative_path = info.filename[len(self.current_dir):]
                if relative_path and "/" not in relative_path.strip("/"):
                    contents.append(relative_path)
        return contents

    def read_file(self, file_path):
        abs_file_path = self.current_dir + file_path.lstrip("/")
        
        # Проверка точных имен файлов для диагностики
        zip_contents = [info.filename for info in self.zip_file.infolist()]
        
        # Проверяем наличие файла в архиве
        if abs_file_path not in zip_contents:
            raise KeyError(f"Файл {abs_file_path} не найден в архиве.")
        
        # Попробуем открыть файл с указанием кодировки
        try:
            with self.zip_file.open(abs_file_path) as file:
                return file.read().decode("utf-8", errors="replace")
        except Exception as e:
            raise

    def find(self, search_name):
        """Ищет файлы и папки по имени внутри zip архива."""
        matching_files = []
        for info in self.zip_file.infolist():
            if "/" + search_name in info.filename:  # Ищем совпадение в имени
                matching_files.append(info.filename)
        return matching_files

    def wc(self, file_path):
        """Возвращает количество строк, слов и символов в файле."""
        try:
            content = self.read_file(file_path)
        except KeyError:
            return "Ошибка: файл не найден."

        lines = content.splitlines()  # Разделяем по строкам
        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)  # Считаем слова
        num_chars = len(content)  # Считаем символы

        return num_lines, num_words, num_chars

    def change_dir(self, path):
        """Изменяет текущую директорию на указанную."""
        if path == "..":
            # Переход в родительскую директорию
            if self.current_dir != 'virtualFS/':  # Не выходим за пределы корневой директории
                self.current_dir = "/".join(self.current_dir.rstrip('/').split('/')[:-1]) + '/'
        elif path.startswith('/'):
            # Абсолютный путь
            new_dir = path.strip('/') + '/'
        else:
            # Относительный путь
            new_dir = os.path.normpath(self.current_dir + '/' + path).replace("\\", "/") + '/'
        
        # Проверяем, что новая директория существует
        if any(info.filename == new_dir and info.is_dir() for info in self.zip_file.infolist()):
            self.current_dir = new_dir
        else:
            raise FileNotFoundError(f"Директория '{path}' не найдена.")
