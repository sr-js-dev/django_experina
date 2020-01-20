# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    fields = ('id', 'order', 'product', 'custom_image', 'custom_color', 'product_name', 'size', 'color', 'price',
              'quantity')
    readonly_fields = ('id',)
    show_change_link = True  # change/edit the Price Object
    extra = 1  # how many empty slots to have for adding a new `Price` from `Product form`
    max_num = 10  # how many `items` for that Product to show in the order list


def send_order_to_customer(modeladmin, request, queryset):  # pragma: no cover
    for order in queryset:
        order.send_email_to_customer()


def send_order_to_admin(modeladmin, request, queryset):  # pragma: no cover
    for order in queryset:
        order.send_email_to_admin()


send_order_to_customer.short_description = "Send Email to Customer"
send_order_to_admin.short_description = "Send Email to Shop Owner"


class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        '__str__',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
    )
    search_fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city')
    inlines = [OrderItemInline, ]
    actions = [send_order_to_admin, send_order_to_customer]


class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product',
        'custom_image',
        'custom_color',
        'product_name',
        'size',
        'color',
        'price',
        'quantity',
        'image',
    )
    list_filter = ('order', 'product')


def _register(model, admin_class):  # pragma: no cover
    admin.site.register(model, admin_class)


_register(models.Order, OrderAdmin)
_register(models.OrderItem, OrderItemAdmin)
