from django.apps import AppConfig


class OnlineClassConfig(AppConfig):
    name = 'online_class'

    def ready(self):
        from updater.update import start
        start()
