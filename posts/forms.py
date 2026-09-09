from . import models
from .models import Banda, Album
from django.forms import ModelForm
from django import forms
from django.shortcuts import get_object_or_404
from durationwidget.widgets import TimeDurationWidget

class GeneroForm(ModelForm):
    class Meta:
        model = models.Genero
        fields = ['genero']
        widgets = {
                    'genero': forms.TextInput(attrs={'class':'form-control'})
        }

class BandaForm(ModelForm):
    class Meta:
        model = models.Banda
        fields = ['banda','pais','logo','generos','estado' ,'descripcion']
        widgets = {
            'banda': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'generos': forms.CheckboxSelectMultiple(),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'logo': forms.ClearableFileInput(attrs={'class': 'custom-file-input-class'}),
            }


class AlbumForm(ModelForm):
    class Meta:
        model = models.Album
        fields = [ 'titulo','miniature', 'tipo', 'generos','anyo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'miniature': forms.ClearableFileInput(attrs={'class':'custom-file-input-class'}),
            'tipo': forms.Select(attrs={'class':'form-select'}),
            'generos': forms.CheckboxSelectMultiple(attrs={'class':'form-select'}),
            'anyo': forms.TextInput(attrs={'class':'form-control'})
        }

    def __init__(self,*args,**kwargs):
        self.banda_id = kwargs.pop('banda_id',None)
        super().__init__(*args,**kwargs)

    def save(self,commit=True):
        album = super().save(commit=False)
        if self.banda_id:
            album.banda = get_object_or_404(models.Banda, pk=self.banda_id)
        if commit:
            album.save()
        return album


class SongForm(ModelForm):
    class Meta:
        model = models.Song
        fields = ['nombre', 'duracion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}), 
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
        }

    def __init__(self,*args,**kwargs):
        self.album_id = kwargs.pop('album_id',None)
        super().__init__(*args,**kwargs)

    def save(self,commit=True):
        song = super().save(commit=False)
        if self.album_id:
            song.album = get_object_or_404(models.Album, pk=self.album_id)
        if commit:
            song.save()
        return song