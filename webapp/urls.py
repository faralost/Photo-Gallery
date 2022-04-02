from django.urls import path

from webapp.views.photo import IndexView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
