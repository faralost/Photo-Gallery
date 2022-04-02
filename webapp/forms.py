from django import forms

from webapp.models import Photo, Album


class PhotoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['album'] = forms.ModelChoiceField(queryset=Album.objects.filter(author=user), required=False)

    class Meta:
        model = Photo
        exclude = ['author', 'favorites']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['author']
