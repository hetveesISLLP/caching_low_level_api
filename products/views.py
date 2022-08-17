from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View

from .models import Product


class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):

        # main logic
        product_objects = cache.get('product_objects')

        if product_objects is None:
            product_objects = Product.objects.all()
            cache.set('product_objects', product_objects)

        # can be used in place of main logic (works same as main logic)
        # product_objects = cache.get_or_set('product_objects', product_objects)

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)


class ProductCreateView(CreateView):
    model = Product
    fields = ['title', 'price']
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('home')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# post_save won't be triggered if you perform an update on the model via a QuerySet:
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['title', 'price']
    template_name = 'products/product_update.html'

    # The post_save signal is triggered if you update an item like so:
    # product = Product.objects.get(id=1)
    # product.title = 'A new title'
    # product.save()

    # we overrode the post method
    # because we have kept signals on save & delete method, so if we write
    # Product.objects.filter(id=1).update(title="A new title"),
    # save/delete method wont be called by default

    # So, in order to trigger the post_save, let's override the queryset update() method.
    # by creating a custom QuerySet and a custom Manager

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        Product.objects.filter(id=self.object.id).update(
            title=request.POST.get('title'),
            price=request.POST.get('price')
        )
        return HttpResponseRedirect(reverse_lazy('home'))


def invalidate_cache(request):
    cache.delete('product_objects')
    url = reverse_lazy('home')
    return HttpResponseRedirect(redirect_to=url)
