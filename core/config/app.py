from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from core.routers import urls
from core.models.ListModels import StaticType
import json
from core.features.search_start import search_for_stop

try:
	with open("settings.json", 'r') as file:
		conf = json.load(file)
except FileNotFoundError:
	conf = {}  # Пустой словарь, если файл не найден
except json.JSONDecodeError:
	conf = {}  # Пустой словарь, если файл содержит некорректный JSON


# class init confif for application
class Config:

	def __init__(self):
		self.origins: List[str] = ["http://localhost", "http://localhost:8080", "http://localhost:8000", "http://localhost:5173"]
		self.static: List[StaticType] = []
		self.urls: List = urls
		self.addOrigin()
		self.addStatic()

		# add new origin
	def addOrigin(self):
		origin = conf.get("origin", [])

		if origin and isinstance(origin, list):
			self.origins.extend(origin)

	# add statics paths for files
	def addStatic(self):
		# Получаем список статических данных из conf, если он существует
		static_data = conf.get("static", [])

		for item in static_data:
			subpath = item.get("subpath")
			directory = item.get("dir")
			name = item.get("name")

			# Проверяем, что значения не пустые и добавляем объект StaticType
			if all((subpath, directory, name)):
				static_obj = StaticType(
					subpath=subpath, dir=directory, name=name)
				self.static.append(static_obj)

		# apply settings from config parameters
	def run(self, app: FastAPI):
		
		search_for_stop(self.origins)

		app.add_middleware(
			CORSMiddleware,
			allow_origins=self.origins,
			allow_credentials=True,
			allow_methods=["*"],
			allow_headers=["*"],
		)

		for static in self.static:
			app.mount("{}".format(static.subpath), StaticFiles(
				directory=static.dir), name=static.name)

		for url in self.urls:
			app.include_router(url, prefix="/api")
