from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import AlbumForm
from webapp.models import Album, Photo


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'album/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_photos'] = self.object.photos.filter(Q(author=self.request.user) | Q(is_private=False)).annotate(
            is_favorited=Exists(Photo.favorites.through.objects.filter(
                user_id=self.request.user.pk,
                photo_id=OuterRef('pk')
            )))
        is_favorited = False
        if self.object.favorites.filter(id=self.request.user.pk).exists():
            is_favorited = True
        context['album_is_favorited'] = is_favorited
        return context


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


class AlbumFavoritesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, pk=kwargs['pk'])
        if album.favorites.filter(id=request.user.pk).exists():
            album.favorites.remove(request.user)
            value = 'добавить в избранное'
        else:
            album.favorites.add(request.user)
            value = 'удалить из избранного'
        data = {
            "value": value
        }
        return JsonResponse(data, safe=False)
