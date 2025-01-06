from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('predict/', views.predict_fraud, name='predict_fraud'),
]