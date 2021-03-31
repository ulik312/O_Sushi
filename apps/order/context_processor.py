from django.contrib.auth import get_user_model

from apps.order.models import Cart, CartItem

User = get_user_model()

def get_cart_items(request):
    if request.user.is_authenticated and request.user.carts.exists():
        user = User.objects.get(email=request.user.email)
        cart = Cart.objects.get(owner=user)
        cart_items = CartItem.objects.filter(cart=cart)
        count = 0
        price_product = 0
        for item in cart_items:
            count += 1
            price_product += (item.product.price * item.qty)
        context = {
            'cart_items_base': cart_items,
            'count_products': count,
            'total_price_product': price_product,
        }
        return context
    return ''