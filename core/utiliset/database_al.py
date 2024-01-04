from alembic import command
from alembic.config import Config
from jinja2 import Template
import inflect
import os

model_template = """
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.config.datebase import Base

class {{class_name}}(Base):
	__tablename__ = '{{ table_name }}'
	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	
__all__ = ['{{class_name}}']
"""

p = inflect.engine()

def alembic_create_migration(message: str, alembic_cfg_path: str = "alembic.ini"):
	"""Создает новую миграцию с заданным сообщением."""
	alembic_cfg = Config(alembic_cfg_path)
	command.revision(alembic_cfg, autogenerate=True, message=message)

def alembic_upgrade(alembic_cfg_path: str = "alembic.ini"):
	"""Применяет все миграции до последней."""
	alembic_cfg = Config(alembic_cfg_path)
	command.upgrade(alembic_cfg, "head")
	
# Функция для создания файла модели
def create_model_file(table_name):
	path = "database\\models"
	
	class_name = table_name.capitalize()
	table_name = p.plural(table_name).lower()

	template = Template(model_template)
	model_content = template.render(class_name=class_name, table_name=table_name)

	if not os.path.exists(path=path):
		os.makedirs(path)
	
	with open(os.path.join(path, table_name.lower() + ".py"), "w") as file:
		file.write(model_content)



