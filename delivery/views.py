import account.forms
from django.utils.decorators import method_decorator

from delivery.models import Order

try:
    import ujson as json
except ImportError:
    import json

# from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
# DetailView, ListView,
from django.views.generic import TemplateView, FormView


#accounts lib
from account.views import LoginView as LoginView_
from account.views import SignupView as SignupView_

#delivery
from delivery.models.Cart import Cart, CartItem, TooBigCartException, TooLowCartException
from delivery.models.Offer import Offer, OutOfStockException
from delivery.models.Profile import Profile
from delivery.models.Address import Address
from delivery.forms import AddToCartForm, CartCheckoutForm


from carousel.models import CarouselPost


class IndexView(TemplateView):
    """Главная"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carousel = CarouselPost.objects.all()
        context['carousel'] = carousel
        return context


class OffersView(TemplateView):
    """Страница списка товаров"""
    template_name = 'offers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offers = Offer.objects.filter(stock__gt=0, hidden=False)
        context['offers'] = offers
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        context['orders'] = Order.objects.filter(cart__user=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    """Страница корзины"""
    template_name = 'cart/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        cart_items = CartItem.objects.filter(cart=cart, quantity__gt=0) # пустые позиции не берем
        context['cart_items'] = cart_items
        context['cart'] = cart
        return context


class CartCheckoutView(FormView):
    template_name = 'cart/checkout.html'
    form_class = CartCheckoutForm
    success_url = '/'

    def form_valid(self, form):
        # метод вызывается после
        # проверки формы на корректность
        # полученных данных
        try:
            cart = Cart.objects.get(user=self.request.user, ordered=False)
            payment_type = form.cleaned_data['payment_type']
            delivery_date = form.cleaned_data['delivery_date']
            address = form.cleaned_data['address']
            order = Order(
                cart=cart,
                address=address,
                delivery_date=delivery_date,
            )
            order.save()
            return HttpResponseRedirect(reverse_lazy('order_success', kwargs={'pk': order.pk}))
        except Cart.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('profile'))

        return super().form_valid(form)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user, ordered=False)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart'] = cart
        return context


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def cart_manage(request):
    """Добавление и удаление позиций в корзине"""

    # различные проверки входящего запроса
    if request.content_type != 'application/json':
        return HttpResponseBadRequest(f'unsupported content type {request.content_type}')
    try:
        data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'status': 'error', 'msg': 'Bad json'}, status=400)

    # сама обработка запроса
    form = AddToCartForm(data)
    if not form.is_valid():
        return JsonResponse({'status': 'error', 'msg': 'You post something bad'}, status=400)
    offer_id = form.cleaned_data.get('offer')
    quantity = form.cleaned_data.get('quantity')
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return JsonResponse({'status': 'error', 'msg': 'Такого товара не существует'}, status=400)

    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
    # в зависимости от типа запроса
    # удаляем или добавляем товар в корзине
    if request.method == "POST":
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, offer=offer)
        try:
            cart_item.increase(amount=quantity)
        except OutOfStockException as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
        except TooBigCartException as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
        return JsonResponse({'status': 'ok', 'msg': "Товар успешно добавлен в корзину"})
    elif request.method == "DELETE":
        cart_item, created = CartItem.objects.get_or_create(cart=cart, offer=offer)
        if created:
            return  JsonResponse({'status': 'error', 'msg': f'В корзину добавлено {quantity} позиций'}, status=400)
        try:
            cart_item.decrease(amount=quantity)
        except TooLowCartException as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
        return JsonResponse({'status': 'ok', 'msg': f'Из корзины удалено {quantity} позиций'})


# CUSTOM AUTH
class LoginView(LoginView_):
    form_class = account.forms.LoginEmailForm


class SignupView(SignupView_):
    identifier_field = 'email'


# Address
class AddressListView(TemplateView):
    template_name = 'profile/address/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context


class AddressUpdateView(UpdateView):
    model = Address
    template_name = 'profile/address/edit.html'
    success_url = reverse_lazy('address_list')
    fields = [
        'city',
        'street',
        'house',
        'apartment',
        'addition',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # проверка принадлежности адреса юзеру
        if context['object'].user != self.request.user:
            raise Http404
        return context


class AddressDeleteView(DeleteView):
    model = Address
    success_url = reverse_lazy('address_list')
    template_name = 'profile/address/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # проверка принадлежности адреса юзеру
        if context['object'].user != self.request.user:
            raise Http404
        return context


class AddressCreateView(CreateView):
    model = Address
    success_url = reverse_lazy('address_list')
    template_name = 'profile/address/create.html'
    fields = [
        'city',
        'street',
        'house',
        'apartment',
        'addition',
    ]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class OrderSuccessView(DetailView):

    template_name = 'profile/order/detail.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # проверка принадлежности адреса юзеру
        object = context['object']
        if object.cart.user != self.request.user:
            raise Http404
        cart_items = CartItem.objects.filter(cart=object.cart)
        print(cart_items)
        context['cart_items'] = cart_items
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context