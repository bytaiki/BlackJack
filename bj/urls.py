from . import views
from django.urls import path

app_name = 'bj'

urlpatterns = [
    path('', views.home ,name='home'),
    path('croom/', views.create_room, name='croom'),
    path('<int:room_id>/lobby/', views.lobby, name='lobby'),
    path('<int:room_id>/start_game', views.start_game, name='start_game'),
    path('on_game/hit', views.hit, name='hit'),
    path('<int:room_id>/result', views.result, name='result'),
    path('<int:room_id>/delete/', views.room_delete, name='room_delete'),
]