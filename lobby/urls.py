from django.urls import path
from . import views

urlpatterns = [
    path('<str:lobby_id>/', views.index, name='index'),
    path('game/', views.game, name='game.index'),
    path('results/', views.results, name='results')
]
