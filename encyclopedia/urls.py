from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>', views.entry, name="entry"),
    path('search/wiki/<str:name>', views.entry, name="entry"),
    path('search/', views.search, name='search'),
    path('create/', views.create, name="create"),
    path('wiki/edit/<str:name>', views.edit, name="edit"),
    path('wiki/e/', views.e, name="e")
]
