from django.urls import path
from .views import HomeView,ClanCreateView,ClanEditView,ClanDeleteView
from .views  import LinkCreateView,LinkEditView,LinkDeleteView,RegisterView,NotificationView,ProfileView,ClanDetailView
from django.contrib.auth.views import LoginView,LogoutView
from .views import join,remove,like,CategoryView,SearchView,remove_notif,remove_all,CommentView,follow
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('clan/<int:pk>/',ClanDetailView.as_view(),name='detail-view'),
    path('clan/create/',ClanCreateView.as_view(),name='clan-create'),
    path('clan/<int:pk>/edit/',ClanEditView.as_view(),name='clan-edit'),
    path('clan/<int:pk>/delete/',ClanDeleteView.as_view(),name='clan-delete'),
    path('clan/<int:pk>/link/add/',LinkCreateView.as_view(),name='link-create'),
    path('clan/<int:pk>/link/edit/',LinkEditView.as_view(),name='link-edit' ),
    path('clan/<int:pk>/link/delete/',LinkDeleteView.as_view(),name='link-delete'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(template_name="Tube/login.html"),name='login'),
    path('logout/', LogoutView.as_view(template_name="Tube/home.html"),name='logout'),
    path('notifs/',NotificationView.as_view(),name='notifs'),
    path('profile/<int:pk>',ProfileView.as_view(),name='profile-view'),
    path('join/',join,name='join'),
    path('remove/',remove,name='remove'),
    path('like/',like,name='like'),
    path('clan/category/', CategoryView.as_view(),name='category-view'),
    path('clan/search/',SearchView.as_view(),name='search-view'),
    path('clan/<int:pk>/comment/',CommentView.as_view(),name='comment'),
    path('follow/',follow,name='follow'),
    
    path('notifs/remove/',remove_notif,name='remove-notif'),
    path('notifs/remove/all/',remove_all, name='remove-all')
]
