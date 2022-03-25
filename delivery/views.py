from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
# Create your views here.
from delivery.models.Cart import Cart, CartItem
from delivery.models.Offer import Offer


"""Index"""
def index(request):
    items = Offer.objects.order_by('id')
    template = loader.get_template('index.html')
    context = {'items': items}
    return HttpResponse(template.render(context, request))

class DetailCart(DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name='cart/detail_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = CartItem.objects.filter(cart=self.get_object())
        return context

class ListCart(ListView):
    model = Cart
    context_object_name = 'carts'
    template_name='cart/list_carts.html'

class CreateCart(CreateView):
    model = Cart
    template_name = 'cart/create_cart.html'

class Updatecart(UpdateView):
    model = Cart
    template_name = 'cart/update_cart.html'

class DeleteCart(DeleteView):
    model = Cart
    template_name = 'cart/delete_cart.html'


##-------------- CartItem Views --------------------------------------
class DetailCartItem(DetailView):
    model = CartItem
    template_name='cartitem/detail_cartitem.html'

class ListCartItem(ListView):
    model = CartItem
    context_object_name = 'cartitems'
    template_name='cartitem/list_cartitems.html'

class CreateItemCart(CreateView):
    model = CartItem
    template_name = 'cartitem/create_cartitem.html'

class UpdateCartItem(UpdateView):
    model = CartItem
    template_name = 'cartitem/update_cartitem.html'

class DeleteCartItem(DeleteView):
    model = Cart
    template_name = 'cartitem/delete_cartitem.html'

