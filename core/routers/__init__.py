import os
import importlib

routers = []
routers_path = "core\\routers"

routers_list = [file for file in os.listdir(routers_path) if file.endswith(".py") and file != "__init__.py"]

for router in routers_list:
	module_name = "core.routers.{}".format(router[:-3])
	module = importlib.import_module(module_name)
	
	if hasattr(module, "routers"):
		routers.extend(module.routers)