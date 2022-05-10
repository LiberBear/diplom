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
from django.views.generic import TemplateView

#accounts lib
from account.views import LoginView as LoginView_
from account.views import SignupView as SignupView_

#delivery
from delivery.models.Cart import Cart, CartItem, TooBigCartException
from delivery.models.Offer import Offer, OutOfStockException
from delivery.forms import AddToCartForm, OfferForm


from carousel.models import CarouselPost



class IndexView(TemplateView):
    """Главная"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carousel = CarouselPost.objects.all()
        template = loader.get_template('index.html')
        context['carousel'] = carousel


@method_decorator(login_required, name='dispatch')
class OffersView(TemplateView):
    """Страница списка товаров"""
    template_name = 'offers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #user = self.request.user
        offers = Offer.objects.all()
        offer_forms = []
        for offer in offers:
            form = OfferForm(instance=offer)
            print(form["img"])
            offer_forms.append(form)
        context['offers'] = offer_forms


@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    """Страница корзины"""
    template_name = 'cart/detail.htmls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart'] = cart


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
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, offer=offer)

    try:
        cart_item.increase(amount=quantity)
    except OutOfStockException as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
    except TooBigCartException as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)

    return JsonResponse({'status': 'ok', 'msg': "Товар успешно добавлен в корзину"})


@login_required
def cart_checkout(request):
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
    cart_items = CartItem.objects.filter(cart=cart)
    #address = Addr
    template = loader.get_template('cart/checkout.html')
    context = {'cart_items': cart_items, 'cart': cart}
    return HttpResponse(template.render(context, request))


# CUSTOM AUTH
class LoginView(LoginView_):
    form_class = account.forms.LoginEmailForm


class SignupView(SignupView_):
    identifier_field = 'email'
