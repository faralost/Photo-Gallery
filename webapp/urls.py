from django.urls import path

from webapp.views.album import (AlbumDetailView,
                                AlbumCreateView,
                                AlbumUpdateView,
                                AlbumDeleteView)

from webapp.views.photo import (IndexView,
                                PhotoDetailView,
                                PhotoCreateView,
                                PhotoUpdateView,
                                PhotoDeleteView,
                                generate_token,
                                PhotoFavoritesView)

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/add/', PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/generate-token/', generate_token, name='photo_generate-token'),
    path('photo/<int:pk>/<token>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('album/add/', AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/update/', AlbumUpdateView.as_view(), name='album_update'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album_delete'),
    path('photo/<int:pk>/favorite', PhotoFavoritesView.as_view(), name="photo_favorite_view"),
]
