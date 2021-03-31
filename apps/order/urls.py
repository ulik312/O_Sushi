from django.urls import path

from .views import *

urlpatterns = [
    path('admin-panel/', IndexAdminView.as_view(), name='index_admin'),
    path('admin-panel/order-detail/1/', order_detail, name='order-detail'),
    path('cart/', CartItemView.as_view(), name='cart'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', DeleteCartItemView.as_view(), name='remove-from-cart'),
    path('change_qty/<int:pk>/', ChangeQuantityView.as_view(), name='change_qty'),
    path('checkout/', OrderCheckoutView.as_view(), name='order_checkout'),
    path('make/', MakeOrderView.as_view(), name='make_order'),
]