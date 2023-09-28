
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
 
 
urlpatterns = [
    path("", views.chatPage, name="chat-page"),
 
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chats/login.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]