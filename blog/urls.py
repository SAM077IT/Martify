from django.urls import path
from .views import BlogView, SingleBlog, PostCategory

urlpatterns = [
    path('', BlogView.as_view(), name="blog"),
    path('<str:post_title>', SingleBlog.as_view(), name="single_post"),
    path('category/<str:category_title>',
         PostCategory.as_view(), name="category_post"),
]
