from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count
from .models import Product, Category
from blog.views import BlogView


class IndexView(View):
    products = Product.objects.all()[:6]
    new_arrival_products = Product.objects.order_by('created_at')[:6]
    categories = Category.objects.annotate(product_count=Count('product'))
    blogs = BlogView.post

    def get(self, request):
        return render(request, "core\index.html", context={'products': self.products, 'new_arrival': self.new_arrival_products, 'categories': self.categories, 'blogs': dict(list(self.blogs.items())[:4]).values()})


class ShopView(View):
    products = Product.objects.all()
    print(products)

    def get(self, request):
        return render(request, "core\category.html", context={"products": self.products})


class CategoryView(View):
    def get(self, request, category):
        category_id = Category.objects.get(name=category).id
        products = Product.objects.filter(category_id=category_id)
        return render(request, "core\category.html", context={"products": products})


class ContactUs(View):
    def get(self, request):
        return render(request, "core\contact.html", context={})


class AboutUs(View):
    def get(self, request):
        return render(request, "core\inabout.html", context={})
