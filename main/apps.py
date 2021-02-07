from django.apps import AppConfig
from . import bhavApi


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        bhavApi.start()
