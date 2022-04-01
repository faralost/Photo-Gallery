from django.urls import path

from webapp.views import Index

app_name = 'webapp'

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
