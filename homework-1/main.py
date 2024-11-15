import tkinter as tk

from shell_emulator.emulatorGUI import ShellEmulatorGUI
from shell_emulator.virtualFS import VirtualFileSystem

if __name__ == "__main__":
    zip_path = "./virtualFS.zip"  # путь к zip-файлу с виртуальной файловой системой
    config_path = "./shell_emulator/config.csv"
    virtual_fs = VirtualFileSystem(zip_path)
    
    root = tk.Tk()
    shell_gui = ShellEmulatorGUI(root, virtual_fs, config_path)
    root.mainloop()
