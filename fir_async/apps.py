from django.apps import AppConfig


class AsyncConfig(AppConfig):
    name = 'fir_async'
    verbose_name = 'Asynchronous plugin'

    def ready(self):
        pass
