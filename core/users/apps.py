from django.apps import AppConfig
from django.db.models.signals import post_migrate


def migrated__add_admins_callback(sender, **kwargs):

    def create_or_skip(username, email, password):
        from core.users.models import User
        try:
            User.objects.get(username=username)
            return
        except User.DoesNotExist:
            User.objects.create_superuser(username, email, password)

    create_or_skip('russ', 'russ.ferriday@gmail.com', 'boldmove')
    create_or_skip('monika', 'harito@haritomedia.com', 'boldmove')


class UsersAppConfig(AppConfig):

    name = "core.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

        # TODO: security - remove this
        post_migrate.connect(migrated__add_admins_callback, sender=self)
