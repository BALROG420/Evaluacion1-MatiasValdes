from django.contrib import admin
from .models import Genero,Tipo,Estado,Banda,Album,Song

from django.db import models
from datetime import timedelta


class GeneroAdmin(admin.ModelAdmin):
    list_display =('genero',)

class TipoAdmin(admin.ModelAdmin):
    list_display =('tipo',)

class EstadoAdmin(admin.ModelAdmin):
    list_display =('estado',)

class BandaAdmin(admin.ModelAdmin):
    list_display =('banda','pais','listar_generos','estado','descripcion','logo')
    def listar_generos(self, objects):
        return ", ".join([g.genero for g in objects.generos.all()])
    listar_generos.short_description = 'generos'

class ListaCanciones(admin.TabularInline):
    model = Song
    extra = 1 

class AlbumAdmin(admin.ModelAdmin):
    list_display =('banda','miniature','titulo','tipo','listar_generos','anyo') 
    inlines = [ListaCanciones]

    def listar_generos(self, objects):
        return ", ".join([g.genero for g in objects.generos.all()])
    listar_generos.short_description = 'generos'    


class SongAdmin(admin.ModelAdmin):
    list_display =('album','nombre','duracion')

# Register your models here.
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Tipo,TipoAdmin)
admin.site.register(Estado,EstadoAdmin)
admin.site.register(Banda,BandaAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Song,SongAdmin)