from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from image_cropping import ImageRatioField


class Size(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Size")
        verbose_name_plural = _("Sizes")


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")


def category_image_upload(instance, filename):
    """

    :param instance: object
    :param filename: str
    :return: str
    """
    return f"categories/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name=_("slug")
    )
    image = models.ImageField(
        upload_to=category_image_upload, verbose_name=_("Category Image")
    )
    cropping = ImageRatioField("image", "300x260", verbose_name=_("image ration"))
    featured = models.BooleanField(default=False, verbose_name=_("is featured"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug
        return super(Category, self).save(*args, **kwargs)


class CustomerImage(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Customer Image")
        verbose_name_plural = _("Customer Images")


class CustomerColor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Customer Color")
        verbose_name_plural = _("Customer Colors")


def product_image_upload(instance, filename):
    return f"products/{filename}"


class Product(models.Model):  # pragma: no cover
    name = models.CharField(max_length=200, verbose_name=_("name"))
    slug = models.SlugField(
        max_length=200, db_index=True, unique=True, verbose_name=_("slug")
    )
    size = models.ManyToManyField(
        Size, related_name="products", verbose_name=_("size"), blank=True
    )
    color = models.ManyToManyField(
        Color, related_name="products", verbose_name=_("color"), blank=True
    )
    category = models.ManyToManyField(
        Category, related_name="products", blank=True, verbose_name=_("categories")
    )
    custom_image = models.BooleanField(
        default=False, verbose_name=_("Customer can choose an Image")
    )
    custom_color = models.BooleanField(
        default=False, verbose_name=_("Customer can choose a Color")
    )
    description = RichTextField(_("description"), null=True, blank=True)
    extra_info = RichTextField(_("extra info"), null=True, blank=True)
    image = models.ImageField(
        upload_to=product_image_upload, verbose_name=_("image from Product Detail Page")
    )
    cropping = ImageRatioField("image", "270x300", verbose_name=_("image ration"))
    cropping_home = ImageRatioField("image", "225x250", verbose_name=_("image ration"))
    cropping_category = ImageRatioField(
        "image", "175x194", verbose_name=_("image ration")
    )
    cropping_related = ImageRatioField("image", "84x93", verbose_name=_("image ration"))
    featured = models.BooleanField(default=False, verbose_name=_("is featured"))
    min_order = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10000), MinValueValidator(1)],
        verbose_name=_("minimum order"),
    )
    related = models.ManyToManyField(
        "self",
        related_name="related_products",
        blank=True,
        verbose_name=_("related products"),
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug
        return super().save(*args, **kwargs)

    def all_variations(self):
        return self.prices.all().order_by("price")

    def get_minimum_price(self):
        minimum_price = None
        prices = self.prices.all().order_by("price")
        if prices:
            minimum_price = prices[0]
        return minimum_price

    def get_minimum_quantity(self):
        minimum_quantity = None
        quantities = self.prices.all().order_by("min_quantity")
        if quantities:
            minimum_quantity = quantities[0]
        return minimum_quantity

    def get_maximum_quantity(self):
        maximum_quantity = None
        quantities = self.prices.all().order_by("-max_quantity")
        if quantities:
            maximum_quantity = quantities[0]
        return maximum_quantity

    def get_maximum_price(self):
        maximum_price = None
        prices = self.prices.all().order_by("-price")
        if prices:
            maximum_price = prices[0]
        return maximum_price

    def get_price(self, quantity=1):
        prices = self.prices.filter(
            min_quantity__lte=quantity, max_quantity__gte=quantity
        ).order_by("price")
        price = self.prices.first()
        if prices:
            price = prices[0]
        return price


class Price(models.Model):  # pragma: no cover
    """Products will have different prices depending on the quantity ordered."""

    product = models.ForeignKey(
        Product,
        related_name="prices",
        on_delete=models.CASCADE,
        verbose_name=_("product"),
    )
    price = models.DecimalField(decimal_places=2, max_digits=7, verbose_name=_("price"))
    min_quantity = models.IntegerField(
        validators=[MaxValueValidator(100000), MinValueValidator(1)],
        verbose_name=_("minimum quantity"),
    )
    max_quantity = models.IntegerField(
        validators=[MaxValueValidator(100000), MinValueValidator(1)],
        verbose_name=_("maximum quanbtity"),
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name="variations",
        verbose_name=_("size"),
        blank=True,
        null=True,
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="variations",
        verbose_name=_("color"),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.price} ({self.min_quantity} - {self.max_quantity})"

    class Meta:
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")


# # connect to redis
# r = redis.StrictRedis(host=settings.REDIS_HOST,
#                       port=settings.REDIS_PORT,
#                       db=settings.REDIS_DB)

# Recommender engine based on what users previously bought together and push other non related
# products that meet the same criteria of asociation like others before.
# class Recommender(object):

#     def get_product_key(self, id):
#         return 'product:{}:purchased_with'.format(id)

#     def products_bought(self, products):
#         product_ids = [p.id for p in products]
#         for product_id in product_ids:
#             for with_id in product_ids:
#                 # get the other products bought with each product
#                 if product_id != with_id:
#                     # increment score for product purchased together
#                     r.zincrby(self.get_product_key(product_id),
#                               with_id,
#                               amount=1)

#     def suggest_products_for(self, products, max_results=6):
#         product_ids = [p.id for p in products]
#         if len(products) == 1:
#             # only 1 product
#             suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
#         else:
#             # generate a temporary key
#             flat_ids = ''.join([str(id) for id in product_ids])
#             tmp_key = 'tmp_{}'.format(flat_ids)
#             # multiple products, combine scores of all products
#             # store the resulting sorted set in a temporary key
#             keys = [self.get_product_key(id) for id in product_ids]
#             r.zunionstore(tmp_key, keys)
#             # remove ids for the products the recommendation is for
#             r.zrem(tmp_key, *product_ids)
#             # get the product ids by their score, descendant sort
#             suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
#             # remove the temporary key
#             r.delete(tmp_key)
#         suggested_products_ids = [int(id) for id in suggestions]

#         # get suggested products and sort by order of appearance
#         suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
#         suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
#         return suggested_products

#     def clear_purchases(self):
#         for id in Product.objects.values_list('id', flat=True):
#             r.delete(self.get_product_key(id))
