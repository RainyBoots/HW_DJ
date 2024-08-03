from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import context
from django.shortcuts import get_object_or_404
from .models import Post
from unidecode import unidecode
from django.db.models import F, Q
 
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
    if request.method == "GET":
        posts = Post.objects.prefetch_related("tags", "category").all().order_by("-published_date")
        search = request.GET.get("search")
    
    if search:
        search_in_title = request.GET.get("search_in_title")
        search_in_text = request.GET.get("search_in_text")
        search_in_tags = request.GET.get("search_in_tags")

        query = Q()

        if search_in_title:
            query |= Q(title__icontains=search)

        if search_in_text:
            query |= Q(text__icontains=search)

        if search_in_tags:
            query |= Q(tags__name__icontains=search)

        if not search_in_title and not search_in_text and not search_in_tags:
            query = Q(text__icontains=search)

        posts = posts.filter(query)
    context = {
        "menu": menu,
        "posts": posts,
        "page_alias": "blog_catalog",
    }
    return render(request, "python_blog/blog.html", context)


def post_detail(request, slug):
    post = Post.objects.prefetch_related("tags", "category").get(slug=slug)
    context = {'post': post,
               'menu': menu}
    if 'viewed_posts' not in request.session:
        request.session['viewed_posts'] = []
        
    if slug not in request.session['viewed_posts']:
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        request.session['viewed_posts'].append(slug)  
        request.session.modified = True
    
        post.refresh_from_db()
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