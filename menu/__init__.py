from fnpdjango.utils.app import AppSettings


class Settings(AppSettings):
    MODULE = 'menu_items'


app_settings = Settings('MENU')
