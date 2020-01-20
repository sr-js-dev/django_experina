from django.views.generic import TemplateView
from apps.products.models import Product, Category


class Homepage(TemplateView):
    """Home page View"""
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        featured_products = Product.objects.filter(featured=True)[:4]
        featured_categories = Category.objects.filter(featured=True)[:3]
        # meta_description = f"With such a range of {Category.objects.count()} categoriues......{}"
        categories = Category.objects.all()
        custom_context = {
            "categories": categories,
            "featured_products": featured_products,
            "featured_categories": featured_categories,
        }
        context.update(custom_context)
        return context


class AboutPage(TemplateView):
    """AboutPage View"""
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        featured_products = Product.objects.filter(featured=True)[:4]
        featured_categories = Category.objects.filter(featured=True)[:3]
        categories = Category.objects.all()
        custom_context = {
            "categories": categories,
            "featured_products": featured_products,
            "featured_categories": featured_categories,
        }
        context.update(custom_context)
        return context


class ContactPage(TemplateView):
    """Contact page View"""
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPage, self).get_context_data(**kwargs)
        featured_products = Product.objects.filter(featured=True)[:4]
        featured_categories = Category.objects.filter(featured=True)[:3]
        categories = Category.objects.all()
        custom_context = {
            "categories": categories,
            "featured_products": featured_products,
            "featured_categories": featured_categories,
        }
        context.update(custom_context)
        return context
