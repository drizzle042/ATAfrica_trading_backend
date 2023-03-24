from django.urls import path
from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('api/v0/main/gen-auth/', views.SigninView.as_view(), name='gen-auth')
]
