from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

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


class AlbumDeleteView(DeleteView):
    model = Album
    template_name = 'album/delete.html'
    success_url = reverse_lazy('webapp:index')
