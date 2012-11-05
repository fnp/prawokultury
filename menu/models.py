import importlib
from . import app_settings

items = importlib.import_module(app_settings.MODULE).ITEMS
