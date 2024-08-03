from django.urls import path
from python_blog import views

urlpatterns = [
    path('', views.blog, name="blog"),
    path('<slug:slug>/', views.post_detail, name="blog_page"),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
]