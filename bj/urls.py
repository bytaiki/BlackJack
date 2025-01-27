from . import views
from django.urls import path

app_name = 'bj'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:user_id>/lobby/', views.lobby, name='lobby'),
    path('<int:user_id>/start_game', views.start_game, name='start_game'),
    path('on_game/hit', views.hit, name='hit'),
    path('<int:user_id>/result', views.result, name='result'),
]