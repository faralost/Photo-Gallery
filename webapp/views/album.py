from django.views.generic import DetailView

from webapp.models import Album


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/detail.html'
