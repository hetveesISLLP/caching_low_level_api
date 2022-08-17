from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet, Manager
from django_lifecycle import LifecycleModel, hook, AFTER_DELETE, AFTER_SAVE
from django.utils import timezone

#  Rather than using database signals, you could use a third-party package called Django Lifecycle,
#  which helps make invalidation of cache easier and more readable

# Django's built-in approach to offering lifecycle hooks is Signals

# Here, we created a custom Manager, which has a single job: To return our custom QuerySet.
# In our custom QuerySet, we overrode the update() method to first delete the cache key and
# then perform the QuerySet update per usual.


class CustomQuerySet(QuerySet):
    def update(self, **kwargs):
        cache.delete('product_objects')
        super(CustomQuerySet, self).update(updated=timezone.now(), **kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)


# if you want to use Signals
# make migrations 'before uncommenting / after commenting'
class Product(models.Model):
    title = models.CharField(max_length=200, blank=False)
    price = models.CharField(max_length=20, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomManager()

    class Meta:
        ordering = ['-created']

# needed if you want to use LifeCycleModel
# make migrations 'before uncommenting / after commenting'

# class Product(LifecycleModel):
#     title = models.CharField(max_length=200, blank=False)
#     price = models.CharField(max_length=20, blank=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     objects = CustomManager()
#
#     class Meta:
#         ordering = ['-created']
#
#     @hook(AFTER_SAVE)
#     @hook(AFTER_DELETE)
#     def invalidate_cache(self):
#         cache.delete('product_objects')
