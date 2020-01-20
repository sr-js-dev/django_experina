# vim: set fileencoding=utf-8 :
from django.contrib import admin
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from image_cropping import ImageCroppingMixin

from apps.products import models


class SizeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    search_fields = ('name',)


class ColorAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    search_fields = ('name',)


class CategoryAdmin(ImageCroppingMixin, admin.ModelAdmin):

    list_display = ('id', 'name', 'slug', 'image', 'featured')
    list_filter = ('featured',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


class CustomerImageAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    search_fields = ('name',)


class CustomerColorAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    search_fields = ('name',)


class PriceInline(admin.TabularInline):
    model = models.Price
    fields = ('id', 'product', 'price', 'min_quantity', 'max_quantity', 'color', 'size')
    readonly_fields = ('id',)
    show_change_link = True  # change/edit the Price Object
    extra = 1  # how many empty slots to have for adding a new `Price` from `Product form`
    max_num = 6  # how many `prices` for that Product to show in the list


def generate_product_variations(modeladmin, request, queryset):
    new_variations_id = []
    for product in queryset:
        sizes = [x for x in product.size.all()]
        colors = [x for x in product.color.all()]
        quantities = [x for x in product.prices.all()]
        for q in quantities:
            for c in colors:
                for s in sizes:
                    variation, created = models.Price.objects.get_or_create(
                        price=q.price,
                        min_quantity=q.min_quantity,
                        max_quantity=q.max_quantity,
                        color=c,
                        size=s,
                        product=product
                    )
                    new_variations_id.append(variation.id)
        models.Price.objects.filter(product=product).exclude(id__in=new_variations_id).delete()
    messages.add_message(request, messages.INFO, _('Variations created.'))


generate_product_variations.short_description = _("Create Product Variations")


class ProductAdmin(ImageCroppingMixin, admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'slug',
        'custom_image',
        'custom_color',
        'description',
        'extra_info',
        'image',
        'featured',
        'min_order',
    )
    list_filter = ('category', 'custom_image', 'custom_color', 'featured')
    # raw_id_fields = ('size', 'color', 'related')
    search_fields = ('name', 'slug')
    inlines = [PriceInline, ]  # pay attention to the `comma` from the `inlines` is required  `,`
    prepopulated_fields = {'slug': ['name']}
    actions = [generate_product_variations,]


class PriceAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'price', 'min_quantity', 'max_quantity')
    list_filter = ('product',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Size, SizeAdmin)
_register(models.Color, ColorAdmin)
_register(models.Category, CategoryAdmin)
_register(models.CustomerImage, CustomerImageAdmin)
_register(models.CustomerColor, CustomerColorAdmin)
_register(models.Product, ProductAdmin)
_register(models.Price, PriceAdmin)
