from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
# from django.db.models import Count
from .models import Blog, BlogCategory
# Create your views here.


class BlogView(View):
    blogs = Blog.objects.all().order_by("-created_at")
    blog_categories = BlogCategory.objects.all()
    post = {}
    for blog in blogs:
        post[blog.id] = {'title': blog.title,
                         'image': blog.image, 'content': blog.post_body[:150], 'day': blog.created_at.day, 'month': blog.created_at, 'slug': blog.title.replace(' ', '-')}

    def get_recent_posts(obj):
        i = 0
        recent_posts = {}
        for blog in obj:
            if i < 2:
                recent_posts[blog.id] = {'title':
                                         blog.title, 'image': blog.image, 'date': blog.created_at}
                i += 1
            else:
                break
        return recent_posts

    recent_posts = get_recent_posts(blogs).values()

    def get(self, request):
        return render(request, "postblog.html", context={'blogs': self.post.values(), 'categories': self.blog_categories, 'recent_posts': self.recent_posts})


class SingleBlog(BlogView):

    def get(self, request, post_title):
        # Replace hyphens with spaces
        post_title = post_title.replace('-', ' ')
        try:
            # Lookup Posts
            blog_post = Blog.objects.get(title=post_title)
        except:
            messages.warning(
                request, "Undefined post! Please try again.")
            return redirect('index')

        return render(request=request, template_name='single_post.html', context={'post': blog_post, 'categories': super().blog_categories, 'recent_posts': super().recent_posts})


class PostCategory(View):
    def get(self, request, category_title):
        post_category = category_title.replace('-', ' ')
        # try:
        #     # Lookup Posts
        blog_category = BlogCategory.objects.get(name=post_category)
        blog_posts = Blog.objects.filter(
            category=blog_category)
        print("Blog: ", blog_posts)
        # except:
        #     messages.warning(
        #         request, "Undefined Category! Please try again.")
        #     return redirect('index')
        post = {}
        for blog in blog_posts:
            post[blog.id] = {'title': blog.title, 'image': blog.image, 'content': blog.post_body[:150],
                             'day': blog.created_at.day, 'month': blog.created_at, 'slug': blog.title.replace(' ', '-')}

        return render(request=request, template_name='category_post.html', context={'posts': post})
