from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('password_change/', views.password_change_request, name='password_change'),
    path('password_change/done/', views.password_change_done_request, name='password_change_done'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_request, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_request, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_request, name='password_reset_complete'),
]