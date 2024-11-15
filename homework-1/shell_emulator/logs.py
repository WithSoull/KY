from datetime import datetime
import csv

class Logger:
    def __init__(self, log_path, username):
        self.log_path = log_path
        self.username = username

    def log_action(self, action):
        with open(self.log_path, 'a', newline='') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, self.username, action])
