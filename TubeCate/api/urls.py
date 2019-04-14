from django.urls import path
from .import views
urlpatterns=[
    path('login/',views.LoginView.as_view()),
    path('register/',views.RegisterView.as_view()),
    path('create/',views.ClanCreateView.as_view()),
    path('home/',views.HomeView.as_view()),
    path('link/<int:pk>/',views.LinkCreateView.as_view()),
    path('clan/like/',views.LikeView.as_view()),
    path('join/<int:pk>/',views.MemberView.as_view()),
    path('profile/<int:pk>/',views.ProfileView.as_view()),
    path('follow/<int:pk>/',views.FollowView.as_view()),
    path('clan/tag/',views.TagSearchView.as_view()),
    path('clan/notif/',views.NotificationView.as_view()),
    path('clan/delete/<int:pk>/',views.ClanDeleteView.as_view()),
    
    #path('clan/edit/<int:pk>/',views.ClanEditView.as_view()),
    path('clan/<int:pk>/',views.ClanDetailView.as_view())
]
