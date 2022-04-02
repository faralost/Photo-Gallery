from django.views.generic import ListView, DetailView

from webapp.models import Photo


class IndexView(ListView):
    template_name = 'photos/index.html'
    model = Photo
    context_object_name = 'photos'
    ordering = ['-created_at']


class PhotoDetailView(DetailView):
    template_name = 'photos/detail.html'
    model = Photo
