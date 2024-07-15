from django.contrib import admin
from django.utils.html import format_html
from django.contrib import admin
from django.urls import reverse
from .models import Customer, Product, Cart, OrderPlaced


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'lacality',
                    'city', 'zipcode', 'state')
    search_fields = ('user__username', 'name', 'city', 'state')
    list_filter = ('state',)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price',
                    'discount_price', 'brand', 'category')
    search_fields = ('title', 'brand', 'category')
    list_filter = ('category', 'brand')
    fields = ('title', 'selling_price', 'discount_price',
              'description', 'brand', 'category', 'product_image')
    readonly_fields = ('id',)


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username', 'product__title')
    list_filter = ('user',)


@admin.register(OrderPlaced)
class OrderModelPlaceAdmin(admin.ModelAdmin):
    # Définition des colonnes à afficher dans la liste des objets
    list_display = ('id', 'user', 'customer', 'customer_info', 'product', 'product_info',
                    'quantity', 'order_date', 'status')

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name, )

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title, )

    # Définition des champs par lesquels la recherche peut être effectuée
    search_fields = ('user__username', 'customer__mane',
                     'product__title', 'status')

    # Ajout de filtres pour la liste des objets
    list_filter = ('status', 'order_date')

    # Définition de l'ordre par défaut des objets dans la liste
    ordering = ('-order_date', 'id')

    # Champs à afficher dans la vue détaillée de chaque objet
    fields = ('user', 'customer', 'product', 'quantity', 'status')

    # Champs en lecture seule (non modifiables) dans la vue détaillée
    readonly_fields = ('order_date',)
