from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='front-login'),
    path('login/', views.signin, name='signin'),
    path('home/', views.home, name='front-home'),
    path('add/', views.add, name='add'),
    path('cargar/', views.cargaMasiva, name='carga'),
    path('peticiones/', views.Peticiones, name = 'peticiones'),
    path('ayuda/', views.Ayuda, name = 'ayuda'  ),
    path('visualizarXML/', views.visualizarXML, name = 'visualizarXML'),
    path('clasificar-por-fecha/', views.clasificacion_por_fecha, name= 'clasificar-por-fecha'),
    path('rango-de-fechas/', views.rango_de_fechas, name= 'rango-de-fechas'),
    path('reporte2/', views.Reporte2, name= 'reporte2'),
    path('reporte3/', views.Reporte3, name= 'reporte3'),
    path('reporte4/', views.Reporte4, name= 'reporte4'),
    path('prueba/', views.Prueba_de_mensaje, name= 'prueba'),
]