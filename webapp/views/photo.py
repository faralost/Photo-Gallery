from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PhotoForm
from webapp.models import Photo


class IndexView(ListView):
    template_name = 'photos/index.html'
    model = Photo
    context_object_name = 'photos'
    ordering = ['-created_at']

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_private=False)


class PhotoDetailView(DetailView):
    template_name = 'photos/detail.html'
    model = Photo


class PhotoCreateView(CreateView):
    template_name = 'photos/create.html'
    form_class = PhotoForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(PhotoCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoUpdateView(UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'photos/update.html'

    def get_form_kwargs(self):
        kwargs = super(PhotoUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'photos/delete.html'
    success_url = reverse_lazy('webapp:index')
