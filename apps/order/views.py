from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils import timezone

from django.views.generic import ListView
from django.views.generic.base import View

from apps.order.models import Cart, CartItem, Order
from apps.product.models import Product

from .forms import OrderForm
from .permissions import SuperUserAdminMixin

User = get_user_model()


class IndexAdminView(SuperUserAdminMixin, ListView):
    model = Order
    template_name = 'order/index_admin_panel.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(IndexAdminView, self).get_queryset()
        today_ = timezone.now().date()
        queryset = queryset.filter(create_at__date=today_).order_by('-create_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['count'] = Order.objects.count()
        return context



def order_detail(request):
    return render(request, 'order/order_detail.html')


class CartItemView(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user)
        cart_items = CartItem.objects.filter(cart=cart)
        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
        return render(request, 'order/cart_checkout.html', context)



class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user, in_order=False)
        product_info = Product.objects.get(pk=product_id)
        CartItem.objects.get_or_create(cart=cart, product=product_info, final_price=product_info.price)
        messages.add_message(request, messages.INFO, 'Продукт успешно добавлен!')
        return redirect('cart')


class DeleteCartItemView(View):

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user, in_order=False)
        product_id = Product.objects.get(pk=product_id)
        cart_product = CartItem.objects.get(cart=cart, product=product_id)
        cart_product.delete()
        cart.save()
        messages.add_message(request, messages.INFO, 'Продукт успешно удален!')
        return redirect('cart')


class ChangeQuantityView(View):

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user, in_order=False)
        product_id = Product.objects.get(pk=product_id)
        cart_product = CartItem.objects.get(cart=cart, product=product_id)
        qty = int(request.POST.get('change_qty'))
        cart_product.qty = qty
        cart_product.final_price = cart_product.product.price * cart_product.qty
        cart_product.save()
        cart.save()
        messages.add_message(request, messages.INFO, 'Количество успешно изменено!')
        return redirect('cart')


class OrderCheckoutView(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user)
        cart_items = CartItem.objects.filter(cart=cart)
        form = OrderForm(request.POST, None)
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'form': form,
        }
        return render(request, 'order/order_checkout.html', context)


class MakeOrderView(View):

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user)
        form = OrderForm(request.POST, None)
        if form.is_valid():
            new_order = form.save(commit=False)
            cart.in_order = True
            new_order.cart = cart
            new_order.customer = user
            new_order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return redirect('index')
        return redirect('order_checkout')


class UpdateOrderAdminView(View):

    def post(self, request, *args, **kwargs):
        pass