from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'

# To use/set up SIGNALS for handling cache invalidation

    def ready(self):
        import products.signals
