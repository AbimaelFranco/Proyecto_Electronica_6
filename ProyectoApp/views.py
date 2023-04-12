from django.shortcuts import render, HttpResponse
import datetime
from getpass import getuser
from ProyectoApp.models import static_panel
import pandas as pd

import random###############################
import time#################################


# Create your views here.

def home(request):
    

    ################################################    
    # query = static_panel.objects.all()
    # print(query)    

    # print(type(query))

    ################################################    
    # datos()
    #################################################

    username = getuser()
    hora = datetime.datetime.now()
    fecha = datetime.date.today()

    if(0<=hora.hour<12):
        mensaje_hora = "Buenos días"
    elif (12<=hora.hour<18):
        mensaje_hora = "Buenas tardes"
    elif (18<=hora.hour<23):
        mensaje_hora = "Buenas noches"


    return render(request, "ProyectoApp/template/index.html",{
        "mensaje_hora": mensaje_hora,
        "username": username,
        "fecha": fecha,
    })

def graph_live(request):

    return render(request, "ProyectoApp/home.html",{})

def graph_history(request):

    return HttpResponse("History")

#####################################################################################

def Voltaje():

    Voltaje = random.randint(1,5)
    print("Voltaje generado: ", Voltaje)

    return Voltaje

def Intensidad():

    Intensidad = random.randint(1,15)
    print("Voltaje generado: ", Intensidad)

    return Intensidad

def generador_datos(Volt, Inten):

     nuevo_registro = static_panel(measurement=Volt, intensity=Inten)
     nuevo_registro.save()          

def datos():
    for i in range(120):
            Volt = Voltaje()
            Inten = Intensidad()
            generador_datos(Volt, Inten)
            time.sleep(10)