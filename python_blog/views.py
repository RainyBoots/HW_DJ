from re import search
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import context
from django.shortcuts import get_object_or_404
from .models import Post
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


posts = [
    {
        "category": "Python",
        "tags": ["основы", "синтаксис", "советы"],
        "slug": "introduction-to-python",
        "title": "Введение в Python",
        "text": ("Python — это высокоуровневый язык программирования с простым синтаксисом и мощными библиотеками. "
                 "Он широко используется для разработки веб-приложений, анализа данных, научных исследований и автоматизации задач. "
                 "Благодаря своей универсальности и поддержке сообщества, Python стал одним из самых популярных языков программирования в мире. "
                 "Кроме того, наличие множества онлайн-курсов и документации делает его отличным выбором для начинающих. "
                 "В этой статье мы рассмотрим основные концепции и примеры использования Python."),
        "author": "Иван Петров",
        "published_date": "2024-06-25",
        "comments": [
            {"author": "Алексей Смирнов", "text": "Отличная статья для новичков!", "date": "2024-06-26"},
            {"author": "Мария Иванова", "text": "Python действительно лучший выбор для начинающих.", "date": "2024-06-27"}
        ]
    },
    {
        "category": "Django",
        "tags": ["веб-разработка", "фреймворк", "приложения"],
        "slug": "getting-started-with-django",
        "title": "Начало работы с Django",
        "text": ("Django — это мощный веб-фреймворк на Python, который позволяет быстро создавать сложные веб-приложения. "
                 "Он включает в себя множество встроенных функций, таких как аутентификация, управление базами данных и административный интерфейс. "
                 "Django следит за принципом DRY (Don't Repeat Yourself), что помогает разработчикам писать чистый и эффективный код. "
                 "Этот фреймворк подходит как для небольших проектов, так и для крупных корпоративных приложений. "
                 "В данной статье мы рассмотрим основные этапы создания проекта на Django и его настройки."),
        "author": "Ольга Кузнецова",
        "published_date": "2024-06-24",
        "comments": [
            {"author": "Сергей Васильев", "text": "Django - отличное решение для стартапов.", "date": "2024-06-25"},
            {"author": "Наталья Соколова", "text": "Статья помогла мне разобраться с настройками.", "date": "2024-06-26"}
        ]
    },
    {
        "category": "Базы данных",
        "tags": ["SQL", "sqlite", "управление"],
        "slug": "database-management-with-sqlite",
        "title": "Управление базами данных с SQLite",
        "text": ("SQLite — это легковесная, но мощная система управления базами данных, которая не требует установки сервера. "
                 "Она идеально подходит для встраиваемых приложений и прототипов, где необходима полноценная реляционная база данных. "
                 "SQLite хранит всю базу данных в одном файле, что упрощает ее перенос и резервное копирование. "
                 "Ее простота и надежность делают SQLite популярным выбором среди разработчиков мобильных и настольных приложений. "
                 "В этой статье мы рассмотрим основные команды SQL и примеры их использования в SQLite."),
        "author": "Анна Сергеева",
        "published_date": "2024-06-23",
        "comments": [
            {"author": "Дмитрий Козлов", "text": "Использую SQLite для небольших проектов, очень удобно!", "date": "2024-06-24"},
            {"author": "Елена Миронова", "text": "Отличное объяснение основных команд SQL.", "date": "2024-06-25"}
        ]
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
        posts = Post.objects.all()
        search = request.GET.get("search")
        search_in_title = request.GET.get("searchInTitle")
        search_in_text = request.GET.get("searchInText")
        search_in_tags = request.GET.get("searchInTags")
        posts_filtered = []
        
        if search:
            
            for post in posts:
                
                # Если чекбоксы выключены, ищем только по тексту
                # Если включен title, ищем по названию
                # Если включен text, ищем по тексту
                # Если включен tags, ищем по тегам
                
                # Поиск по умолчанию
                if not search_in_title and not search_in_text and not search_in_tags:
                    if search.lower() in post["text"].lower():
                        posts_filtered.append(post)

                # Поиск по названию
                if search_in_title:
                    if search.lower() in post["title"].lower():
                        posts_filtered.append(post)

                # Поиск по тексту
                if search_in_text:
                    if search.lower() in post["text"].lower():
                        posts_filtered.append(post)
                
                # Поиск по тегам
                if search_in_tags:
                    for tag in post["tags"]:
                        if search.lower() in tag.lower():
                            posts_filtered.append(post)

                
    
        context = {
            "menu": menu,
            "posts": posts_filtered if posts_filtered else posts,
            "page_alias": "blog_catalog",
        }
        return render(request, "python_blog/blog.html", context)


def blog_page(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post,
               'menu': menu}
    return render(request, 'python_blog/post_detail.html', context=context)
