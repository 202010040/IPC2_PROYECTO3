import os
from distutils.log import error
from pathlib import Path
from pickle import FALSE
from tkinter import font
from unittest import result
from urllib import response
from weasyprint.text.fonts import FontConfiguration
from django.conf import settings
import pdfkit
# Create your views here.
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from weasyprint import CSS, HTML

from . import wsgi
from .forms import AddForm, DateForm2, FileForm, LoginForm, DateForm

endpoint= 'http://127.0.0.1:5000/'

from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


#Funcion de rendeizar el reporte
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

#NUEVO CODIGO

def cargaMasiva(request):
    ctx = {
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'CargaMasiva', data=xml_binary)
            if response.ok:
                ctx['response'] = xml
                response = response.json()
                return render(request, 'carga.html', response)
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
                response = response.json()
                return render(request, 'carga.html', response)
        response = response.json() 
        return render(request, 'carga.html', response)

    if request.method == 'GET': #NO BORRAR
        response = requests.get(endpoint + 'CargaMasiva');
        response = response.json()
        return render(request, 'carga.html', response)

#-------------------- MENU DE PETICIONES -------------------------
def Peticiones(request):
    if request.method == "GET":
        return render(request, 'peticiones.html')

#VER LA ENTRADA Y SALIDA DE LA CONSULTA DE DATOS
def visualizarXML(request):
    #EN LA WEB...
    if request.method == "GET":
        response = requests.get(endpoint + 'consultar');
        response = response.json()
        return render(request,'visualizarXML.html',response)
    #EN EL REPORTE...
    if request.method == "POST":
        response = requests.get(endpoint + 'consultar');
        context = response.json()
        html = render_to_string("Reporte1.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; report.pdf"
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)
        return response
#CLASIFICACION POR FECHA
def clasificacion_por_fecha (request):
    #EN A WEB
    #VER EL FORMULARIO PARA CLASIFICAR FECHA
    if request.method == "GET":
        contexto  = requests.get(endpoint + 'clasificar-por-fecha')
        contexto = contexto.json()
        return render (request, 'Clasificacion por fecha.html', contexto)
    if request.method == "POST":
        formulario = DateForm(request.POST)
        json = {
            'date':formulario['date'].value(),
            'empresa':formulario['empresa'].value()
        }
        context = requests.post(endpoint + 'clasificar-por-fecha', json=json)
        context = context.json()
        return render (request, 'Clasificacion por fecha2.html', context)

#CLASIFICACION POR FECHA
def rango_de_fechas (request):
    #EN A WEB
    #VER EL FORMULARIO PARA CLASIFICAR FECHA
    if request.method == "GET":
        contexto  = requests.get(endpoint + 'resumen-por-rango')
        contexto = contexto.json()
        return render (request, 'Resumen por rango.html', contexto)
    if request.method == "POST":
        formulario = DateForm2(request.POST)
        json = {
            'date1':formulario['date1'].value(),
            'date2':formulario['date2'].value(),
            'empresa':formulario['empresa'].value()
        }
        context = requests.post(endpoint + 'resumen-por-rango', json=json)
        context = context.json()
        print(context)
        return render (request, 'Resumen por rango2.html', context)

#Reportes 2 y 3
def Reporte2(request):
    #EN EL REPORTE...
    if request.method == "POST":
        response = requests.post(endpoint + 'reporte2');
        context = response.json()
        html = render_to_string("Reporte2.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Visualizacion.pdf"
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)
        return response

def Reporte3(request):
    #EN EL REPORTE...
    if request.method == "POST":
        response = requests.post(endpoint + 'reporte3');
        context = response.json()
        html = render_to_string("Reporte3.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Rango.pdf"
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)
        return response

def Reporte4(request):
    #EN EL REPORTE...
    if request.method == "POST":
        response = requests.post(endpoint + 'reporte4');
        context = response.json()
        html = render_to_string("Reporte1.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "inline; Rango.pdf"
        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, font_config=font_config)
        return response

def Prueba_de_mensaje(request):
    ctx = {
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + '/prueba-de-mensaje', data=xml_binary)
        response = response.json() 
        return render(request, 'Prueba de mensaje.html', response)

    if request.method == 'GET':
        return render(request, 'Prueba de mensaje.html')

def Reset (request):
    if request.method == 'POST':
        ctx = requests.post(endpoint + '/reset')
        return render(request, 'base.html', ctx.json())

def Ayuda (request):
    if request.method == "GET":
        return render(request,'ayuda.html')
