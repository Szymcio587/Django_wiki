from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.entry, name="entry"),
    path('search/wiki/<str:name>', views.entry, name="entry"),
    path('search/', views.search, name='search'),
    path('create/', views.create, name="create"),
    path('add/', views.add, name="add")
]
