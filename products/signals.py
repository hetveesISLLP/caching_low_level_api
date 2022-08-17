from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Product
# Here, we used the receiver decorator from django.dispatch to decorate functions that get called when a
# product is added or deleted, respectively

# @receiver:
# first argument is the signal event in which to tie the decorated function to, either a save or delete
# second argument is sender, the Product model in which to receive signals from.
# third argument is a string as the dispatch_uid to prevent duplicate signals.


@receiver(post_delete, sender=Product, dispatch_uid='post_deleted')
def object_post_delete_handler(sender, **kwargs):
    cache.delete('product_objects')


@receiver(post_save, sender=Product, dispatch_uid='posts_updated')
def object_post_save_handler(sender, **kwargs):
    cache.delete('product_objects')
