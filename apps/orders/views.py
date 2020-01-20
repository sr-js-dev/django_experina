from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from apps.products.models import Product, Category
from apps.orders.models import Cart, Order, OrderItem
from apps.orders.forms import CreateOrderForm, CartAddProductForm


@csrf_protect
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, instance=product)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            size=cd.get("size"),
            color=cd.get("color"),
            custom_image=cd.get("custom_image"),
            custom_color=cd.get("custom_color"),
            quantity=cd.get("quantity"),
            update_quantity=cd.get("update_quantity"),
        )

    messages.success(request, _("Product added to your Shopping Bag."))
    return redirect("cart_detail")


@csrf_protect
def cart_update(request, product_id):
    cart = Cart(request)
    quantity = request.POST.get("quantity")
    next = request.POST.get("next")
    product = get_object_or_404(Product, id=product_id)
    try:
        quantity = int(quantity)
    except ValueError:
        raise ValueError(
            {"invalid_quantity": f"Provided quantity value {quantity} is invalid"}
        )

    cart.update(product=product, quantity=quantity)
    messages.success(request, _("Product updated to your Shopping Bag."))
    return redirect(next)


@csrf_protect
def cart_remove(request, product_id):
    next = request.POST.get("next")
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.warning(request, _("Product removed from your Shopping Bag."))
    return redirect(next)


class OrderCreateView(CreateView):
    model = Order
    template_name = "orders/order-details.html"
    form_class = CreateOrderForm

    def get_success_url(self):
        cart = Cart(self.request)
        success_url = reverse("homepage")
        order = self.object
        for cart_item in cart:
            product = cart_item["product"]
            OrderItem.objects.create(
                order=order,
                product=product,
                custom_image=cart_item["custom_image"],
                custom_color=cart_item["custom_color"],
                product_name=product.name,
                size=cart_item["size"],
                color=cart_item["color"],
                price=cart_item["price"],
                quantity=cart_item["quantity"],
                image=product.image,
            )
        # clear the cart
        cart.clear()
        message = _(
            f"Order no. #0{order.id} successfully registered. You will receive an email with further instructions."
        )
        messages.add_message(self.request, messages.SUCCESS, message)
        order.send_email_to_customer()
        order.send_email_to_admin()
        return success_url

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        categories = Category.objects.all()
        custom_context = {"categories": categories, "cart": cart}
        context.update(custom_context)
        return context


class CartDetailView(TemplateView):
    template_name = "orders/cart-details.html"

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        categories = Category.objects.all()
        custom_context = {"categories": categories, "cart": cart}
        context.update(custom_context)
        return context
