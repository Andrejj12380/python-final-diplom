from django.apps import AppConfig


class BackendConfig(AppConfig):
    name = 'backend_orders'

    def ready(self):
        """
        импортируем сигналы
        """
