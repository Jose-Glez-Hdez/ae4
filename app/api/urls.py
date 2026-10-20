from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio),
    path("healthz", views.healthz),
    path("api/mensaje", views.mensaje),
    path("api/visitas", views.visitas),
    path("api/lugares", views.lugares),
    path("api/login", views.login),
]