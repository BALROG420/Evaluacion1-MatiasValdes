from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
import datetime
import openpyxl
from openpyxl.drawing.image import Image


from .models import Banda, Album, Genero
from .forms import BandaForm, AlbumForm, SongForm, GeneroForm
# Create your views here.
def index(request):
    bandas = Banda.objects.all()
    return render(request, 'posts/index.html',context={'bandas': bandas})  

def banda_detalle(request, banda_id):
    banda = get_object_or_404(Banda, pk=banda_id)
    return render(request, 'posts/banda_detalle.html', {'banda': banda})

def album_detalle(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    canciones = album.songs.all()
    duracion_total = sum((s.duracion for s in canciones), datetime.timedelta())
    return render(request, 'posts/album_detalle.html', {'album': album, 'duracion_total': str(duracion_total)})
    


def publicar_post(request):
    if request.method == 'POST':
        form = BandaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = BandaForm()

    return render(request, 'posts/banda_form.html', {'form': form})


def publicar_album(request, banda_id):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, banda_id=banda_id)
        if form.is_valid():
            form.save()
            return redirect('posts:banda_detalle', banda_id=banda_id)
    else:
        form = AlbumForm(banda_id=banda_id)

    return render(request, 'posts/album_form.html', {'form': form,'banda_id': banda_id})


def publicar_canciones(request, album_id):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, album_id=album_id)
        if form.is_valid():
            form.save()
            return redirect('posts:album_detalle', album_id=album_id)
    else:
        form = SongForm(album_id=album_id)

    return render(request, 'posts/songs_form.html', {'form': form,'album_id': album_id})


def editar_banda(request,banda_id):
    banda = get_object_or_404 (Banda, pk=banda_id)
    if request.method == 'POST':
        form = BandaForm(request.POST, request.FILES,instance=banda)
        if form.is_valid():
            form.save()
            return redirect('posts:album_detalle', banda_id=banda.id)
    else:
        form = BandaForm(instance=banda)

    return render(request, 'posts/banda_form.html',{'form': form})        

def borrar_banda(request, banda_id):
    genero = get_object_or_404(Banda, pk=banda_id)
    if request.method == 'POST':
        genero.delete()
    return redirect('posts:index')




def generos (request):
    generos = Genero.objects.all()
    editar = request.GET.get('editar') == '1'
    form = GeneroForm()
    return render(request,'posts/generos.html', {'generos': generos, 'editar': editar, 'form': form})

def agregar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/generos/?editar=1')

def editar_genero(request, genero_id):
    genero = get_object_or_404(Genero, pk=genero_id)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
    return redirect('/generos/?editar=1')

def borrar_genero(request, genero_id):
    genero = get_object_or_404(Genero, pk=genero_id)
    if request.method == 'POST':
        genero.delete()
    return redirect('/generos/?editar=1')




def albumexportexcel(request,album_id):
    album = get_object_or_404(Album, pk=album_id)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Canciones'

    ws.column_dimensions['A'].width = 35
    ws.row_dimensions[1].height = 20

    if album.miniature:
        img = Image(album.miniature.path)
        img.width = 250
        img.height = 250 
        ws.add_image(img, f'A1')


    ws.append(['','#', 'Titulo', 'Duracion'])

    for i, song in enumerate(album.songs.all(),start=1):
        ws.append(['',i,song.nombre,str(song.duracion)])

    response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{album.titulo}.xlsx"'
    wb.save(response)
    return response