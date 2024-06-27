from django.urls import path
from python_blog import views

urlpatterns = [
    path('', views.blog, name="blog"),
    path('<slug:slug>/', views.blog_page, name="blog_page"),
]