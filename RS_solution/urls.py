from django.urls import path
from . import views


urlpatterns = [
    path('', views.map, name='map'),
    path('update_charts/', views.update_charts, name='update_charts'),
    # path('reset_map/', views.reset_map, name='reset_map'),
   
]