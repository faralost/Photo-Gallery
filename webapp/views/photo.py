from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'photos/index.html'
    model = Photo
    context_object_name = 'photos'
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().filter(Q(author=self.request.user) | Q(is_private=False))


class PhotoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'photos/detail.html'
    model = Photo


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
