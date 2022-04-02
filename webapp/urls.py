from django.urls import path

from webapp.views.album import AlbumDetailView
from webapp.views.photo import (IndexView,
                                PhotoDetailView,
                                PhotoCreateView,
                                PhotoUpdateView,
                                PhotoDeleteView,)

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/add/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
]
