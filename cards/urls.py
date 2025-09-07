
from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('cards/', views.cards_list, name='cards_list'),
    path('quiz/', views.quiz, name='quiz'),
    path('upload/', views.upload_cards, name='upload_cards'),
    path('add/', views.add_card, name='add_card'),
]
