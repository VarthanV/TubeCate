from django.urls import path
from .views import LoginView,RegisterView,ClanCreateView,HomeView,LinkCreateView
urlpatterns=[
    path('login/',LoginView.as_view()),
    path('register/',RegisterView.as_view()),
    path('create/',ClanCreateView.as_view()),
    path('home/',HomeView.as_view()),
    path('link/',LinkCreateView.as_view())
]