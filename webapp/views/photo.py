from secrets import token_urlsafe

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Exists, OuterRef
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'photos/index.html'
    model = Photo
    context_object_name = 'photos'
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().filter(Q(author=self.request.user) | Q(is_private=False)).annotate(
            is_favorited=Exists(Photo.favorites.through.objects.filter(
                user_id=self.request.user.pk,
                photo_id=OuterRef('pk')
            ))
        )


class PhotoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'photos/detail.html'
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_favorited = False
        if self.object.favorites.filter(id=self.request.user.pk).exists():
            is_favorited = True
        context['photo_is_favorited'] = is_favorited
        return context

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        print(token)
        print(self.get_object().token)
        if token:
            if self.get_object().token != token:
                return HttpResponse('У вас нет доступа к этому ресурсу! Возможно ваш токен невалиден', status=400)
        return super().get(request, *args, **kwargs)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    template_name = 'photos/create.html'
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PhotoCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'webapp.change_photo'
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/update.html'

    def get_form_kwargs(self):
        kwargs = super(PhotoUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'webapp.delete_photo'
    model = Photo
    template_name = 'photos/delete.html'
    success_url = reverse_lazy('webapp:index')

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


def generate_token(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if not photo.token:
        photo.token = token_urlsafe()
        photo.save()
    return redirect('webapp:photo_detail', pk=pk)


class PhotoFavoritesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        if photo.favorites.filter(id=request.user.pk).exists():
            photo.favorites.remove(request.user)
            value = 'добавить в избранное'
        else:
            photo.favorites.add(request.user)
            value = 'удалить из избранного'
        data = {
            "value": value
        }
        return JsonResponse(data, safe=False)
