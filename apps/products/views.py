import operator
from functools import reduce
from django.db.models import Q
from apps.orders.forms import CartAddProductForm
from django.views.generic import DetailView, ListView
from apps.products.models import Category, Product, CustomerImage, CustomerColor
from apps.orders.models import Cart


class CategoryProductsList(DetailView):
    template_name = "products/category_products.html"
    queryset = Category.objects.all()
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super(CategoryProductsList, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        categories = Category.objects.all()
        custom_context = {"categories": categories, "cart": cart}
        context.update(custom_context)
        return context


class ProductDetails(DetailView):
    template_name = "products/product_detail.html"
    queryset = Product.objects.all()
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)

        instance = context.get("object", None)
        form = CartAddProductForm(self.request.POST, instance=instance)

        customer_images = CustomerImage.objects.all()
        customer_colors = CustomerColor.objects.all()
        cart = Cart(self.request)
        categories = Category.objects.all()
        custom_context = {
            "categories": categories,
            "customer_images": customer_images,
            "customer_colors": customer_colors,
            "cart": cart,
            "form": form,
        }
        context.update(custom_context)
        return context


class SearchProductsList(ListView):
    template_name = "products/search_products.html"
    queryset = Product.objects.all()
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super(SearchProductsList, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        categories = Category.objects.all()
        q_term = self.request.GET.get("q")
        custom_context = {"cart": cart, "q_term": q_term, "categories": categories}
        context.update(custom_context)
        return context

    def get_queryset(self):
        q_list = self.request.GET.get("q").split(" ") or []
        by_name = reduce(operator.or_, [Q(name__icontains=q) for q in q_list])
        by_category = reduce(
            operator.or_, [Q(category__name__icontains=q) for q in q_list]
        )
        by_size = reduce(operator.or_, [Q(size__name__icontains=q) for q in q_list])
        by_color = reduce(operator.or_, [Q(color__name__icontains=q) for q in q_list])
        queryset = Product.objects.filter(
            by_name | by_category | by_size | by_color
        ).distinct()
        return queryset
