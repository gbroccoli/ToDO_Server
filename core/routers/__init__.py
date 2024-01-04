import os
from importlib import import_module

urls = []

path_urls = "core\\routers"

list_urls = [item for item in os.listdir(path_urls) if item.endswith(".py") and item != "__init__.py"]

for item in list_urls:
    module_name = "core.routers.{}".format(item[:-3])
    
	# Загружаем модуль
    module = import_module(module_name)

    # Проверяем наличие атрибута 'routers' в модуле
    if hasattr(module, "routers"):
        # Если атрибут существует, добавляем его содержимое в список 'urls'
        urls.extend(module.routers)