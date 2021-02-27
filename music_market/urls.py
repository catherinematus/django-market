from django.urls import path
from . import views
from .views import home_page, product_category, product_subcategory, product_detail,\
    product_to_basket, product_in_basket, product_remove_basket, product_leave_basket, login_user, register, review, \
    add_review, delivery, payment

urlpatterns = [

    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('category/<int:pk_category>/', product_category, name='product_category'),
    path('subcategory/<int:pk_subcategory>/', product_subcategory, name='product_subcategory'),
    path('product_detail/<int:product_pk>', product_detail, name='product_detail'),
    path('product_detail/<int:product_pk>/to_buy', product_to_basket, name='product_to_basket'),
    path('product_detail/<int:product_pk>/not_to_buy', product_remove_basket, name='product_remove_basket'),
    path('product_detail/<int:product_pk>/leave', product_leave_basket, name='product_leave_basket'),
    path('product_in_basket/', product_in_basket, name='product_in_basket'),
    path('product_to_basket/order/<int:basket_pk>/', views.order, name='order'),
    path('review/', review, name='review'),
    path('add_review/', add_review, name='add_review'),
    path('delivery/', delivery, name='delivery'),
    path('payment/', payment, name='payment'),

    path('', home_page, name='home_page'),

]
