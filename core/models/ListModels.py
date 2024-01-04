from typing import NamedTuple, Optional, Union

# Модель для описания словарей, включенных в список статических файлов
# Model for describing dictionaries included in the list of static files


class StaticType(NamedTuple):
    subpath: str
    dir: str
    name: str


class EnvMain(NamedTuple):
    title: str
    debug: bool
    version: str
    redoc_url: Optional[Union[None, str]] = None
