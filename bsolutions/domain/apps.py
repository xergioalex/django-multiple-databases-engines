from django.apps import AppConfig


class DomainConfig(AppConfig):
    name = 'bsolutions.domain'
    verbose_name = "Domain"

    def ready(self):
        import bsolutions.domain.signals
