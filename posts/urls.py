from django.urls import path
from . import views

app_name='posts'
urlpatterns =[
    path('',views.index,name='index'),
    path('generos/',views.generos, name='generos'),
    path('generos/agregar/', views.agregar_genero, name='agregar_genero'),
    path('generos/<int:genero_id>/editar/', views.editar_genero, name='editar_genero'),
    path('generos/<int:genero_id>/borrar/', views.borrar_genero, name='borrar_genero'),

    path('banda/<int:banda_id>/', views.banda_detalle, name='banda_detalle'),
    path('banda/<int:banda_id>/editar/', views.editar_banda, name='editar_banda'),
    path('banda/<int:banda_id>/borrar/', views.borrar_banda, name='borrar_banda'),

    path('album/<int:album_id>/', views.album_detalle, name='album_detalle'),

    path('form/banda',views.publicar_post,name='form_banda'),
    path('form/album/<int:banda_id>/',views.publicar_album,name='form_album'),
    path('form/song/<int:album_id>/',views.publicar_canciones,name='form_song'),
    path('album/<int:album_id>/exportar/', views.albumexportexcel, name='exportar_album'),
]   