from django.urls import path  # type: ignore[import-untyped]
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/<slug:service_name>/',
         views.service_detail,
         name='service_detail'),
    path('category/<slug:master_slug>/',
         views.master_detail,
         name='master_detail'),
]
