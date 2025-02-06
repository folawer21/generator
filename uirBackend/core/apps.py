from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        # Запуск файла при инициализации приложения
        # Путь к файлу с моковыми данными
        mock_data_file = os.path.join(self.path, 'fill_mock_models.py')
        
        if os.path.exists(mock_data_file):
            # Используем exec(), чтобы выполнить скрипт
            with open(mock_data_file, 'r') as file:
                exec(file.read())
    