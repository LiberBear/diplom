import account.forms
from django.utils.decorators import method_decorator

try:
    import ujson as json
except ImportError:
    import json

# from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, FormView

#accounts lib
from account.views import LoginView as LoginView_
from account.views import SignupView as SignupView_

#delivery
from delivery.models.Cart import Cart, CartItem, TooBigCartException, TooLowCartException
from delivery.models.Offer import Offer, OutOfStockException
from delivery.models.Profile import Profile
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
        offers = Offer.objects.all()
        context['offers'] = offers
        return context


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
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
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user, ordered=False)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart'] = cart
        return context


@csrf_exempt
@login_required
@require_http_methods(["POST", "DELETE"])
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
