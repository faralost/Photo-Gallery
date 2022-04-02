from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'album/detail.html'


class AlbumCreateView(LoginRequiredMixin, CreateView):
    template_name = 'album/create.html'
    form_class = AlbumForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'webapp.change_album'
    model = Album
    form_class = AlbumForm
    template_name = 'album/update.html'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class AlbumDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'webapp.delete_album'
    model = Album
    template_name = 'album/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author
