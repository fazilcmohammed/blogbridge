from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup-page'),
    path('login/', views.loginn, name='login-page'),
    path('home/', views.home, name='home-page'),
    path('newpost/', views.newPost, name='new-post'),
    path('mypost/', views.myPost, name='my-post'),
    path('signout/', views.signout, name='signout-btn'),
    path('edit/<int:id>/', views.edit_post, name='edit-post'),
    path('delete/<int:id>/', views.delete_post, name='delete-post'),
    path('post/<int:id>/', views.read_post, name='read-post'),
]