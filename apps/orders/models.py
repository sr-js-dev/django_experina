from decimal import Decimal
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext as _
from apps.products.models import Product

# django.conf.settings is the Django settings.py file and also our own settings/__init__.py


class Order(models.Model):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    email = models.EmailField(_("e-mail"))
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("postal code"), max_length=20)
    city = models.CharField(_("city"), max_length=100)
    remarks = models.TextField(_("remarks"), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):  # pragma: no cover
        return _(f"Order {self.id}")

    @property
    def total_order(self):  # pragma: no cover
        total = sum([item.price for item in self.items.all()])
        return Decimal(total) or 0.00

    def send_email_to_customer(self):  # pragma: no cover
        subject = _(f"Order no. #0{self.id} successfully registered")
        email_from = settings.EMAIL_SENDER_NAME
        email_to = [self.email]
        message = _(
            f"Hi {self.first_name}, \n\n Your Order no. #0{self.id} was successfully registered.\n\nYou will soon be contacted by someone from our Sales Department in order to discuss further details about delivery and payment.\n\n\n\n\n\nBest regards,\nexperina.nl Team"
        )
        send_mail(subject, message, email_from, email_to, fail_silently=False)

    def send_email_to_admin(self):  # pragma: no cover
        subject = _(f"New Order placed: no. #0{self.id}")
        email_from = settings.EMAIL_SENDER_NAME
        email_to = ["johan@johanboerema.nl", "sportpriis@experina.nl"]
        # Delete admin emails from the list but keep
        # commented ones for later 'johan@johanboerema.nl', 'catalin.coroeanu@icloud.com'
        message = _(
            f"Hi there, \n\n You have a new Order from {self.first_name} {self.last_name} ({self.email}). \n\nOrder no. #0{self.id} of total value: € {self.total_order}\n\n\n\n\n\n Best regards,\nYour trustworthy Notification Robot"
        )
        send_mail(subject, message, email_from, email_to, fail_silently=False)


def orders_image_upload(instance, filename):  # pragma: no cover
    return f"orders/{filename}"


class OrderItem(models.Model):  # pragma: no cover
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name=_("order")
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("product"),
    )
    custom_image = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("custom image")
    )
    custom_color = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("custom color")
    )
    product_name = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("product name")
    )
    size = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("color")
    )
    color = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("postal code")
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("price"))
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(100000)], verbose_name=_("quantity")
    )
    image = models.ImageField(upload_to=orders_image_upload, verbose_name=_("image"))

    def __str__(self):
        return f"Order Item {self.id}"

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")


class Cart(object):  # pragma: no cover
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        self.user = request.user

        cart = self.session.get(settings.CART_SESSION_ID)
        if cart:
            product_ids = cart.keys()
            Product.objects.filter(id__in=product_ids)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.total_items = len(self.cart)

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            item["size"] = item["size"]
            item["color"] = item["color"]
            item["custom_image"] = item["custom_image"]
            item["custom_color"] = item["custom_color"]
            yield item

    def is_product_in_cart(self, product_id):
        try:
            self.cart[product_id]
        except KeyError:
            return False
        return True

    def add(
        self,
        product,
        size,
        color,
        custom_image,
        custom_color,
        quantity=1,
        update_quantity=False,
    ):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": quantity,
                "price": str(product.get_price(quantity).price),
                "size": size,
                "color": color,
                "custom_image": custom_image,
                "custom_color": custom_color,
            }
        else:
            self.cart[product_id]["quantity"] += 1
            self.cart[product_id]["price"] = str(
                product.get_price(self.cart[product_id]["quantity"]).price
            )
        self.save()

    def update(self, product, quantity=1):
        """
        Update a product: update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 1}
        else:
            self.cart[product_id]["quantity"] = quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.cart = {}
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
