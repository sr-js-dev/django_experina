from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from apps.pages.views import Homepage, AboutPage, ContactPage
from apps.products.views import CategoryProductsList, ProductDetails, SearchProductsList
from apps.orders.views import (
    cart_add,
    cart_update,
    cart_remove,
    OrderCreateView,
    CartDetailView,
)


def health_check(request):
    return JsonResponse({"response": "ok"})


urlpatterns = i18n_patterns(
    *[
        path("about/", AboutPage.as_view(), name="about"),
        path("contact/", ContactPage.as_view(), name="contact"),
        path("search/", SearchProductsList.as_view(), name="search"),
        path("health-check/", health_check, name="health"),
        path(
            "category/<slug:slug>/",
            CategoryProductsList.as_view(),
            name="category_products",
        ),
        path("product/<slug:slug>/", ProductDetails.as_view(), name="product_details"),
        path("cart/detail/", CartDetailView.as_view(), name="cart_detail"),
        path("cart/add/<int:product_id>/", cart_add, name="cart_add"),
        path("cart/update/<int:product_id>/", cart_update, name="cart_update"),
        path("cart/remove/<int:product_id>/", cart_remove, name="cart_remove"),
        path("order/", OrderCreateView.as_view(), name="create_order"),
        path("admin/", admin.site.urls),
        path("", Homepage.as_view(), name="homepage"),
    ],
    prefix_default_language=False
)


if settings.ENV in ["local"]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
