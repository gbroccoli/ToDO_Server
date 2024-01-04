from os import listdir
from importlib import import_module

imported_models = []

models_directory = "database\\models"

model_files = [
    file
    for file in listdir(models_directory)
    if file.endswith(".py") and file != "__init__.py" and file != "models.py"
]

for model in model_files:
    module_name = f"database.models.{model[:-3]}"
    module = import_module(module_name)

    modules_names = getattr(
        module, "__all__", [
            name for name in dir(module) if not name.startswith("_")])

    imported_models.extend(
        [getattr(module, modul_name) for modul_name in modules_names]
    )
