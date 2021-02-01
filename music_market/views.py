from django.shortcuts import render, get_object_or_404
from .models import Category, Subcategory, Product, Image, Basket, ProductInBasket, Order, Review
from .forms import ContactForm, LoginForm, RegisterUserForm, ReviewForm
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home_page(request):
    categorys = Category.objects.all()
    username = auth.get_user(request).username
    if request.user.is_authenticated:
        try:
            basket = Basket.objects.get(user=request.user)
            basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
        except ObjectDoesNotExist:
            basket = Basket.objects.create(user=request.user)
            basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
    else:
        basket = 0
        basket_products = 0
    return render(request, 'product/home_page.html', {'categorys': categorys,
                                                      'username': username,
                                                      'basket': basket,
                                                      'basket_products': basket_products,
                                                      })


def product_category(request, pk_category):
    category = get_object_or_404(Category, pk=pk_category)
    subcategorys = Subcategory.objects.filter(category=category)
    if request.user.is_authenticated:
        basket = get_object_or_404(Basket, user=request.user.id)
        basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
    else:
        basket = 0
        basket_products = 0
    return render(request, 'product/subcategories.html', {'subcategorys': subcategorys,
                                                          'basket': basket,
                                                          'basket_products': basket_products,
                                                          'category': category,
                                                          })


def product_subcategory(request, pk_subcategory):
    subcategory = get_object_or_404(Subcategory, pk=pk_subcategory)
    products = Product.objects.filter(subcategory=subcategory)
    if request.user.is_authenticated:
        basket = get_object_or_404(Basket, user=request.user.id)
        basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
    else:
        basket = 0
        basket_products = 0
    return render(request, 'product/product_list.html', {'products': products,
                                                         'basket': basket,
                                                         'basket_products': basket_products,
                                                         'subcategory': subcategory,
                                                         })


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    images = Image.objects.filter(product=product)
    if request.user.is_authenticated:
        basket = get_object_or_404(Basket, user=request.user.id)
        basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
    else:
        basket = 0
        basket_products = 0
    return render(request, 'product/product_detail.html', {'product': product,
                                                           'images': images,
                                                           'basket': basket,
                                                           'basket_products': basket_products,
                                                           })


def product_to_basket(request, product_pk):
    if request.user.is_authenticated:
        try:
            basket = Basket.objects.get(user=request.user)
        except ObjectDoesNotExist:
            basket = Basket.objects.create(user=request.user)

        product = get_object_or_404(Product, pk=product_pk)

        try:
            pib = ProductInBasket.objects.get(basket=basket, product=product)
            pib.count += 1
            pib.save()
        except ObjectDoesNotExist:
            pib = ProductInBasket.objects.create(basket=basket, product=product, count=1)
        return redirect('product_in_basket')
    else:
        return redirect('login_user')


def product_in_basket(request):
    if request.user.is_authenticated:
        basket = get_object_or_404(Basket, user=request.user.id)
        products = ProductInBasket.objects.filter(basket__id=basket.id)
        basket_products = ProductInBasket.objects.filter(basket_id=basket.id)
        return render(request, 'product/product_in_basket.html', {'products': products,
                                                                  'basket': basket,
                                                                  'basket_products': basket_products,
                                                                  })
    else:
        return redirect('login_user')


def product_remove_basket(request, product_pk):
    pib = get_object_or_404(ProductInBasket, pk=product_pk)
    if pib.count > 1:
        pib.count -= 1
    pib.save()
    return redirect('product_in_basket')


def product_leave_basket(request, product_pk):
    product = get_object_or_404(ProductInBasket, pk=product_pk)
    product.delete()
    return redirect('product_in_basket')


def order(request, basket_pk):
    basket = get_object_or_404(Basket, pk=basket_pk)
    basket_products = ProductInBasket.objects.filter(basket_id=basket.id)

    if request.method == 'POST':
        order = Order.objects.filter(basket=basket).last()
        list_products = [el.product for el in order.products]
        list_counts = [el.count for el in order.products]
        list_order = dict(zip(list_products, list_counts))
        total_price = order.basket.total_price
        total_price = f'{total_price}'
        form = ContactForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_products = ' '.join('{0} - {1} шт.,'.format(key, val) for key, val in list_order.items())
            order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ. Мы Вам позвоним.')
            pib = ProductInBasket.objects.filter(basket__id=basket.id).delete()
            return redirect('home_page')
    else:
        order = Order.objects.create(basket=basket)
        total_price = order.basket.total_price
        total_price = f'{total_price}'
        list_products = [el.product for el in order.products]
        list_counts = [el.count for el in order.products]
        list_order = dict(zip(list_products, list_counts))
        form = ContactForm(instance=order)

    return render(request, 'product/order.html', {'list_order': list_order,
                                                  'total_price': total_price,
                                                  'form': form,
                                                  'basket_products': basket_products,
                                                  })


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home_page')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form})


def review(request):
    reviews = Review.objects.all()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'product/reviews.html', {'reviews': reviews,
                                                            'form': form,
                                                            })
    else:
        form = ReviewForm()
    return render(request, 'product/reviews.html', {'reviews': reviews,
                                                    'form': form,
                                                    })


