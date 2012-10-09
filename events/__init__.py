from fnpdjango.utils.app import AppSettings


class Settings(AppSettings):
    BOX_LENGTH = 3


app_settings = Settings('EVENTS')
