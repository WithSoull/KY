import unittest
from shell_emulator.emulatorGUI import ShellEmulatorGUI
from shell_emulator.virtualFS import VirtualFileSystem
from shell_emulator.config import ShellConfig
import tkinter as tk
import os

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Настройка окружения для тестов
        cls.root = tk.Tk()
        cls.config_path = "tests/config.csv"  # путь к конфигурации
        cls.virtual_fs_path = "tests/testFS.zip"  # путь к тестовому виртуальному ФС zip
        cls.virtual_fs = VirtualFileSystem(cls.virtual_fs_path)
        cls.gui = ShellEmulatorGUI(cls.root, cls.virtual_fs, cls.config_path)

        print(cls.virtual_fs.list_dir())

    def test_ls_root_directory(self):
        # Проверяем команду 'ls' для корневой директории
        output = self.virtual_fs.list_dir()
        expected_output = ['empty.txt', 'folder/', 'test.txt']
        self.assertEqual(sorted(output), sorted(expected_output))

    def test_ls_folder(self):
        # Проверяем команду 'ls' для пустой папки
        self.virtual_fs.current_dir = "folder"  # Переходим в папку 'folder'
        output = self.virtual_fs.list_dir()
        expected_output = ['nested.txt']  # Папка должна содержать только один файл
        self.assertEqual(sorted(output), sorted(expected_output))

    def test_ls_empty_folder_in_root(self):
        # Проверяем команду 'ls' для пустой папки
        self.virtual_fs.current_dir = "empty_folder"  # Переходим в пустую папку
        output = self.virtual_fs.list_dir()
        expected_output = []  # Папка пустая
        self.assertEqual(sorted(output), sorted(expected_output))


    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == "__main__":
    unittest.main()
