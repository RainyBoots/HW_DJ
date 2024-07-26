from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import context
from django.shortcuts import get_object_or_404
from .models import Post
from unidecode import unidecode 
menu = [
    {
        "name": "Главная",
        "url": "/",
        "alias": "main"
    },
    {
        "name": "Блог",
        "url": "/blog/",
        "alias": "blog"
    },
    {
        "name": "О проекте",
        "url": "/about/",
        "alias": "about"
    }
]



def home_page(request):
    context = {'menu': menu,
               'page_alias': 'main'}
    return render(request, 'main.html', context=context)


def about(request):
    context = {'menu': menu,
               'page_alias': 'about'}
    return render(request, 'about.html', context=context)



def blog(request):
    posts = Post.objects.all()
    context = {
        "menu": menu,
        "posts": posts,
        "page_alias": "blog_catalog",
    }
    return render(request, "python_blog/blog.html", context)


def blog_page(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post,
               'menu': menu}
    return render(request, 'python_blog/post_detail.html', context=context)


def category_detail(request, slug: str):
    posts = posts = Post.objects.filter(category__slug=slug)
    context = {
        "menu": menu,
        "posts": posts,
    }

    return render(request, "python_blog/blog.html", context)


def tag_detail(request, slug: str):
    posts = Post.objects.filter(tags__slug=slug)
    context = {
        "menu": menu,
        "posts": posts,
    }

    return render(request, "python_blog/blog.html", context)