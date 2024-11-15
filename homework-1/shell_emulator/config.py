import csv

class ShellConfig:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            reader = csv.reader(file)
            config = next(reader)  # Предполагаем, что данные на одной строке
            
            self.username = config[0]
            self.path_to_zip_fs = config[1]
            self.path_to_log_file = config[2]
            self.path_to_start_script = config[3]
