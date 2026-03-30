from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import Http404
from django.db.models import Count
from .models import Product, Category
from blog.views import BlogView


class IndexView(View):
    products = Product.objects.all()[:6]
    new_arrival_products = Product.objects.order_by('created_at')[:6]
    categories = Category.objects.annotate(product_count=Count('product'))
    blogs = BlogView.post

    def get(self, request):
        return render(request, "core/index.html", context={'products': self.products, 'new_arrival': self.new_arrival_products, 'categories': self.categories, 'blogs': dict(list(self.blogs.items())[:4]).values()})


class ShopView(View):
    products = Product.objects.all()

    def get(self, request):
        return render(request, "core/category.html", context={"products": self.products})


class CategoryView(View):
    def get(self, request, category):
        category_id = Category.objects.get(name=category).id
        products = Product.objects.filter(category_id=category_id)
        return render(request, "core/category.html", context={"products": products})


class ProductView(View):
    def get(self, request, product):
        # Convert URL-friendly format (underscores) to actual product name
        product_name = product.replace("_", " ")

        # Get product with case-insensitive fallback
        try:
            product_details = Product.objects.get(name__iexact=product_name)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")
        # Get related products from same category (excluding current product)
        related_products = Product.objects.filter(
            category=product_details.category
        ).exclude(id=product_details.id)[:4]

        return render(request, "core/product.html", context={
            "product_details": product_details,
            "related_products": related_products
        })


class ContactUs(View):
    def get(self, request):
        return render(request, "core/contact.html", context={})


class AboutUs(View):
    def get(self, request):
        return render(request, "core/page_about.html", context={})
