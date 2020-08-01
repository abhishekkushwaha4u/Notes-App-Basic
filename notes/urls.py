from django.urls import path
from . import views
urlpatterns = [
    path('user', views.UserRegistrationView.as_view()),
    path('user/auth', views.UserLoginView.as_view()),
    path('sites/list/', views.UserNotesListView.as_view()),
    path('sites', views.AddNoteView.as_view()),
]
