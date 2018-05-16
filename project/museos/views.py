import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Museo, MuseoSeleccionado, Comentario, Css
from django.contrib.auth import logout, login
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
import urllib.request

def userLog(request):
    user = False
    if request.user.is_authenticated():
        respuesta = "Logged in as " + request.user.username + ". "
        respuesta += '<a href="/logout">Logout</a>'
    else:
        respuesta = "Not logged in. " + '<a href="/login">Login</a>'
    return respuesta

def usuariosLat(request):
    # Muestra los enlaces a páginas personales en columna lateral
    luser = []
    luserObj = MuseoSeleccionado.objects.all()
    for a in luserObj:
        add = a.usuario
        if add not in luser:
            luser.append(add)
    return luser

@csrf_exempt
def parsear(request):
    munimadrid = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
    xml = urllib.request.urlopen(munimadrid)
    tree = ET.parse(xml)
    root = tree.getroot()
    cont = 0
    for neighbor in root.iter('atributos'):
        email,phone,num, descrip,hora, bus = "", "", "","", "", ""
        for filaBD in neighbor.iterfind('atributo'):
            #dic = filaBD.attrib
            for elem in filaBD.attrib:
                if elem.find('atributo'):
                    for x in filaBD.iterfind('atributo'):
                        for varsDir in x.attrib:
                            if x.attrib[varsDir]=="CLASE-VIAL":
                                via = ' '.join(x.itertext())
                            elif x.attrib[varsDir]== "NOMBRE-VIA":
                                street = ' '.join(x.itertext())
                            elif x.attrib[varsDir]== "NUM":
                                num = ' '.join(x.itertext())
                            elif x.attrib[varsDir]== "CODIGO-POSTAL":
                                postal = ' '.join(x.itertext())
                            elif x.attrib[varsDir]== "LOCALIDAD":
                                city = ' '.join(x.itertext())
                            elif x.attrib[varsDir]=="LATITUD":
                                lat=' '.join(x.itertext())
                            elif x.attrib[varsDir]=="LONGITUD":
                                l = ' '.join(x.itertext())
                            elif x.attrib[varsDir]=="BARRIO":
                                bar = ' '.join(x.itertext())
                            elif x.attrib[varsDir]=="DISTRITO":
                                district = ' '.join(x.itertext())
                            elif x.attrib[varsDir]=="TELEFONO":
                                phone = ' '.join(x.itertext())
                            elif x.attrib[varsDir]=="EMAIL":
                                email = ' '.join(x.itertext())
                if filaBD.attrib[elem]=="NOMBRE":
                    name = ' '.join(filaBD.itertext())
                elif filaBD.attrib[elem]=="CONTENT-URL":
                    url = ' '.join(filaBD.itertext())
                elif filaBD.attrib[elem]=="ACCESIBILIDAD":
                    access = int(' '.join(filaBD.itertext()))
                elif filaBD.attrib[elem]=="DESCRIPCION-ENTIDAD":
                    descrip = ' '.join(filaBD.itertext())
                elif filaBD.attrib[elem]=="HORARIO":
                    hora = ' '.join(filaBD.itertext())
                elif filaBD.attrib[elem]=="TRANSPORTE":
                    bus = ' '.join(filaBD.itertext())
        address = " ".join([via, street, num, postal, city])
        contenido = Museo(id=cont,nombre=name,url=url,direccion=address,latitud=lat,longitud=l,descripcion=descrip,horario=hora, busMetro=bus, accesible=access,barrio=bar,distrito=district,email=email,tlfno=phone)
        contenido.save()
        cont = cont +1
    lMuseosParseada = Museo.objects.all()
    print(lMuseosParseada)
    return lMuseosParseada

@csrf_exempt
def principal(request):
    acceso = 0
    cruz = 'unchecked'
    luser = []
    user = request.user.username
    regUsuarios = userLog(request)
    lMuseos = Museo.objects.all().order_by("-ncomment")[:5]
    titulo = " Los museos almacenados son:"
    if request.method == 'POST':
        acceso=request.POST.get('Accesible')
        if request.user.is_authenticated():
            user = request.user.username
            validar = request.POST.get('_submit')
            print(validar)
            #if 'enviar' in request.POST:
            #    validar = 1
            if validar or not len(lMuseos):
                print("eo")
                lMuseos = parsear(request)
                lMuseos = Museo.objects.all() #.order_by("-ncomment")[:5]
    if acceso:
        lMuseos = Museo.objects.filter(accesible=acceso)
        cruz = 'checked'
    # Muestra los enlaces a páginas personales en columna lateral
    luserObj = MuseoSeleccionado.objects.all()
    for a in luserObj:
        add = a.usuario
        if add not in luser:
            luser.append(add)
    plantilla = get_template("htmlCss/index.html")
    c = Context({'name': titulo, 'listaMuseo': lMuseos, 'users': luser, 'login': regUsuarios, 'acceso':cruz, 'usuario': user})
    return HttpResponse(plantilla.render(c))

@csrf_exempt
def usuario(request, recurso):
    background = '#efefef'
    regUsuarios = userLog(request)
    lusers = usuariosLat(request)
    cuerpo = request.body
    user = recurso.split('/')[0]
    userReg = request.user.username
    respuesta = "Página de usuario"
    if request.method == 'GET':
        try:
            lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)
        except MuseoSeleccionado.DoesNotExist:
            respuesta += recurso + " no tiene museos seleccionados"
    elif request.method == 'POST':
        lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)[:5]
        if request.user.is_authenticated() and userReg == user:
            #user = request.user.username
            cssForm = request.POST.get('css')
            if cssForm == 'Cambiar':
                background = request.POST['fondo']
                size = request.POST['letraTam']
                title = request.POST['titulo']
                try:
                    cssObj = Css.objects.get(usuario=user)
                    if user == cssObj.usuario:
                        idcss = cssObj.id
                        print(idcss)
                        cssObj = Css.objects.get(id=idcss)
                        cssObj.tamLetra=size
                        cssObj.colorFondo=background
                        cssObj.titulo=title
                        #contenido = cssObj(tamLetra=size, colorFondo=background, titulo=title)
                        cssObj.save()
                        css(request)
                        print('vamos')
                except:
                    t= "Pagina de " + user
                    contenido = Css(usuario=user, tamLetra=size, colorFondo=background ,titulo=t)
                    contenido.save()
                #redirect('/' + user)
            else:
                if 'enviar' in request.POST:
                    #ap_id = int(request.POST.get['enviar'])
                    cuerpo = request.body.decode('utf-8')
                    ap_id = int(cuerpo.split('=')[-1])
                    ko = MuseoSeleccionado.objects.get(museo=ap_id) #get
                    ko.delete()
        if len(lMuseoUser) > 5:
            lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)[5:10]
    plantilla = get_template("htmlCss/usuario.html")
    c = RequestContext(request,{'listaMuseo': lMuseoUser, 'content':respuesta, 'login': regUsuarios, 'users': lusers, 'usuario':user, 'bg':background})
    return HttpResponse(plantilla.render(c))

def user_xml(request, recurso):
    user = recurso.split('/')[0]
    lMuseoUser = MuseoSeleccionado.objects.filter(usuario=user)
    hijos = serializers.serialize("xml" ,lMuseoUser)
    f = open('usuario.xml',"w")
    f.write(hijos)
    f.close()
    f2 = open('usuario.xml',"r")
    xml = f2.read()
    return HttpResponse(xml, content_type='text/xml')

@csrf_exempt
def css(request):
    if request.user.is_authenticated():
        user = request.user.username
        css = Css.objects.get(usuario=user)
    plantilla = get_template("htmlCss/style.css")
    c = Context({'varsCss': css.colorFondo })
    #redirect('static/style.css')
