from django.views.generic import DetailView, CreateView, UpdateView

from webapp.forms import AlbumForm
from webapp.models import Album


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'album/detail.html'


class AlbumCreateView(CreateView):
    template_name = 'album/create.html'
    form_class = AlbumForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'album/update.html'
