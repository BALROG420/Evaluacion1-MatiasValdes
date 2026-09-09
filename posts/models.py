from django.db import models
from datetime import timedelta


class Genero(models.Model):
    genero = models.CharField(max_length=130, unique=True)

    def __str__(self):
        return self.genero


class Tipo(models.Model):
    tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipo


class Estado(models.Model):
    estado = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.estado


class Banda(models.Model):
    banda = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    generos = models.ManyToManyField(Genero)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    logo = models.ImageField(upload_to='posts/logo')

    def __str__(self):
        return self.banda


class Album(models.Model):
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='albums')
    miniature = models.ImageField(upload_to='posts/miniatures')
    titulo = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True)
    generos = models.ManyToManyField(Genero)
    anyo = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.titulo


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    nombre = models.CharField(max_length=130)
    duracion = models.DurationField(default=timedelta(minutes=0, seconds=0))

    def __str__(self):
        return self.nombre
