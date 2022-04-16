from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

# Create your views here.
from delivery.models.Cart import Cart, CartItem
from delivery.models.Offer import Offer
from carousel.models import CarouselPost
#from django.db.models import F

from delivery.forms import AddToCartForm, OfferForm


def index(request):
    """Главная"""
    carousel = CarouselPost.objects.all()
    template = loader.get_template('index.html')
    context = {'carousel': carousel}
    return HttpResponse(template.render(context, request))


@login_required
def offers_page(request):
    """Страница списка товаров"""
    user = request.user
    offers = Offer.objects.all()
    offer_forms = []
    for offer in offers:
        form = OfferForm(instance=offer)
        print(form["img"])
        offer_forms.append(form)
    template = loader.get_template('offers.html')
    context = {'offers': offer_forms}
    return HttpResponse(template.render(context, request))

#     user = self.request.user
#     current_cart = Cart.objects
#     queryset = CartItem.objects.all().order_by("id")
#     serializer_class = OfferSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['title', 'desc']
#     ordering_filters = ['title']
#
#     def get_user(self):
# #
# class DetailCart(DetailView):
#
#     model = Cart
#     context_object_name = 'cart'
#     template_name = 'cart/detail_cart.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart = self.get_object()
#         context['cart_items'] = CartItem.objects.filter(cart=cart)
#         context["cart"] = cart
#         return context
# def add_to_cart(request):
#
#     if request.method == 'POST':
#         form = AddToCartForm(request.POST)
#         if form.is_valid():
#             print(request.POST)
#             print("form valid")
#             print(form.cleaned_data)
#             url = form.cleaned_data.get("referer", "/")
#             print(url)
#             return redirect(url)
#         else:
#             print(form.errors())
#             #form = AddToCartForm()
#     return redirect("/")
#
# class ListCart(ListView):
#     model = Cart
#     context_object_name = 'carts'
#     template_name = 'cart/list_carts.html'
#
#
# class CreateCart(CreateView):
#     model = Cart
#     template_name = 'cart/create_cart.html'
#
#
# class Updatecart(UpdateView):
#     model = Cart
#     template_name = 'cart/update_cart.html'
#
#
# class DeleteCart(DeleteView):
#     model = Cart
#     template_name = 'cart/delete_cart.html'
#
#
# ##-------------- CartItem Views --------------------------------------
# class DetailCartItem(DetailView):
#     model = CartItem
#     template_name = 'cartitem/detail_cartitem.html'
#
#
# class ListCartItem(ListView):
#     model = CartItem
#     context_object_name = 'cartitems'
#     template_name = 'cartitem/list_cartitems.html'
#
#
# class CreateItemCart(CreateView):
#     model = CartItem
#     template_name = 'cartitem/create_cartitem.html'
#
#
# class UpdateCartItem(UpdateView):
#     model = CartItem
#     template_name = 'cartitem/update_cartitem.html'
#
#
# class DeleteCartItem(DeleteView):
#     model = Cart
#     template_name = 'cartitem/delete_cartitem.html'
