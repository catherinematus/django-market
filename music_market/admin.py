from django.contrib import admin
from .models import Product, Category, Subcategory, Image, Basket, ProductInBasket, Order, Review

# admin.site.register(Product)
# admin.site.register(Image)

class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

    inlines = [ProductImageInline]

    class Meta:
         model = Product

admin.site.register(Product, ProductAdmin )

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Basket)


# admin.site.register(ProductInBasket)
# admin.site.register(Order)

class ProductInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
         model = ProductInBasket

admin.site.register(ProductInBasket, ProductInBasketAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

    class Meta:
         model = Order

admin.site.register(Order, OrderAdmin)

admin.site.register(Review)


