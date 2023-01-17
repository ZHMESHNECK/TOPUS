from django.apps import AppConfig


class TanksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tanks'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import tanks.signals
