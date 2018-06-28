import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Museo, MuseoSeleccionado, Comentario, Css
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.db.models import Count
import urllib.request

def userLog(request):
    user = False
    if request.user.is_authenticated():
        respuesta = "Logged in as " + request.user.username + ". "
        respuesta += '<a href="/logout">Logout</a>'
    else:
        respuesta = "Not logged in. " + '<a href="/login">Login</a>'
    return respuesta
####
def registroUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect('/')
            #else:
            # Return a 'disabled account' error message
        #else:
        # Return an 'invalid login' error message.


def usuariosLateral():
    # Muestra los enlaces a páginas personales en columna lateral
    luser = []
    luserObj = MuseoSeleccionado.objects.all()
    for a in luserObj:
        add = a.usuario
        if add not in luser:
            luser.append(add)
    return luser
#####
def cssLateral(request,user):
    luserCss = []
    lusers = usuariosLateral()
    if not user in lusers:
        luserCss = Css.objects.order_by('id').order_by('titulo')
        #addTitle = Css.objects.get(usuario=usuarioReg)
        #luserCss.append(addTitle.titulo)
        print(luserCss)

    return luserCss


def mostrar5(request, mus):
    if request.method == 'GET':
        # Se muestran los museos del usuario de 5 en 5
        QS = request.GET
        tanda = QS.get('numPage',default=0)
        tanda = int(tanda)
        try:
            lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)
            if len(lMuseoUser) >= tanda*5:
                numPag = range(5,len(lMuseoUser),5)
                print(len(lMuseoUser), str(tanda))
                lMuseoUser = lMuseoUser[tanda*5:(tanda+1)*5]
                tanda += 1
                print(numPag)
                #numPag.append(tanda)
        except MuseoSeleccionado.DoesNotExist:
            titulo = recurso + " no tiene museos seleccionados"

@csrf_exempt
def parsear(request):
    madridDat = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
    xml = urllib.request.urlopen(madridDat)
    # https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree
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
        contenido = Museo(id=cont,nombre=name,url=url,direccion=address,
                          latitud=lat,longitud=l,descripcion=descrip,
                          horario=hora, busMetro=bus, accesible=access,
                          barrio=bar,distrito=district,email=email,tlfno=phone)
        contenido.save()
        cont = cont +1
    lMuseosParseada = Museo.objects.all()
    return lMuseosParseada

def cargaMuseosComentados():
    lcomment = Comentario.objects.all()
    for museo in lcomment:
        add = museo.museo_id
        museoComentado = Museo.objects.get(id=add)
        museoComentado.ncomment += 1
        museoComentado.save()


def cargaMuseosSeleccionados():
    num_veces = 0
    lista = []
    #lMuseoSel = MuseoSeleccionado.objects.order_by('museo_id__id').
    #lMuseoSel = MuseoSeleccionado.objects.select_related('museo_id').get(id=int(museo_id))
    lMuseoSel = Museo.objects.annotate(num_veces=Count('museoseleccionado')).order_by('-num_veces')
    print(lMuseoSel[0].num_veces,lMuseoSel[1].num_veces)
    return lMuseoSel


@csrf_exempt
def principal(request):
    acceso = 0
    lMuseos = None
    lusers = usuariosLateral()
    user = request.user.username
    background = css(request,user)
    lusersCss = cssLateral(request,user)
    regUsuarios = userLog(request)
    titulo = " Los museos más seleccionados son:"
    if request.method == 'GET':
        ## Elimina los museos no comentados de la lista y solo muestra 5
        # lMuseos = Museo.objects.exclude(ncomment=False)[:5]
        # lMuseos = []

        if not lMuseos:
            lParse = parsear(request)
        lMuseos = cargaMuseosSeleccionados()[:5]
    elif request.method == 'POST':
        oculto = request.POST.get('next')
        if not oculto:
            acceso=request.POST.get('Accesible')
            lMuseos = Museo.objects.filter(accesible=acceso)
        if request.user.is_authenticated(): # Solo cargan usuarios registrados
            validar = request.POST.get('_submit')
            print(validar)
            #if validar or not len(lMuseos):
            if validar != None:
                lParse = parsear(request)
                # cargaMuseosComentados()
                # lMuseos = Museo.objects.exclude(ncomment=False)[:5]
                lMuseos = cargaMuseosSeleccionados()[:5]

        else:
            titulo = "No está registrado. No puede cargar los museos"
            return redirect(principal)
    plantilla = get_template("htmlCss/index.html")
    c = Context({'name': titulo, 'listaMuseos': lMuseos,'login': regUsuarios,
                 'users': lusersCss, 'acceso':acceso, 'usuario': user,
                 'bg':background})
    return HttpResponse(plantilla.render(c))


@csrf_exempt
def museos_all(request):
    dis = {}
    lDistritos = []
    lusers = usuariosLateral()
    user = request.user.username
    background = css(request,user)
    regUsuarios = userLog(request)
    titulo = "Todos los museos son:"
    if request.method == 'GET':
        lMuseos = Museo.objects.all()
        # Crea la lista de distritos para filtrar
        for m in lMuseos:
            addDistrito = m.distrito
            if addDistrito not in lDistritos:
                lDistritos.append(addDistrito)
        QS = request.GET
        dis = QS.get('distrito',default=None)
        # Para filtrar sin contar espacios a partir de la QueryString
        if dis:
            lMuseos = Museo.objects.filter(distrito__startswith=dis)
    elif request.method == 'POST':
        #filtro = request.POST.get('filtro')
        #if filtro != None:
        lMuseos = Museo.objects.all()
        puntua=request.POST.get('puntua')
        print(puntua)
        if puntua:
            museo_id = int(puntua)
            info = Museo.objects.get(id=museo_id)
            info.puntuacion += 1
            info.save()
        if request.user.is_authenticated():
            if '_submit' in request.POST:
                museo_id = int(request.POST['_submit'])
                lMuseoSelect = MuseoSeleccionado.objects.all()
                ko = MuseoSeleccionado.objects.filter(museo=museo_id)
                ko = ko.filter(usuario=user)
                print(ko)
                if not len(ko):

                    info = Museo.objects.get(id=museo_id)
                    addMuseo = MuseoSeleccionado(usuario=user, museo=info)
                    addMuseo.save()
    plantilla = get_template("htmlCss/museos.html")
    c = Context({'listaMuseos': lMuseos, 'name': titulo, 'login': regUsuarios,
                 'users': lusers, 'listDistrito': lDistritos, 'usuario': user,
                 'bg':background})
    return HttpResponse(plantilla.render(c))


@csrf_exempt
def museo_id(request, museo_id):
    regUsuarios = userLog(request)
    lusers = usuariosLateral()
    user = request.user.username
    background = css(request,user)
    museo_id = int(museo_id.split('/')[-1])
    titulo = "Página de museo seleccionado. "
    info = None
    if request.method == 'GET':
        try:
            info = Museo.objects.get(id=museo_id)
            comentarios = Comentario.objects.filter(museo=museo_id)
        except Museo.DoesNotExist:
            titulo = "Museo no almacenado"
        except Comentario.DoesNotExist:
            titulo += "No tiene comentarios."
    elif request.method == 'POST':
        if request.user.is_authenticated():
            com = request.POST['comment']
            info = Museo.objects.get(id=museo_id)
            addcom = Comentario(contenido=com, museo=info)
            addcom.save()
            info.ncomment += 1
            info.save()
    enlace = request.get_host() ######
    comentarios = Comentario.objects.filter(museo=museo_id)
    plantilla = get_template("htmlCss/museo_id.html")
    c = RequestContext(request,{'name': titulo, 'museum': info, 'users': lusers,
                                'login':regUsuarios, 'lcomment':comentarios,
                                'usuario': user, 'bg':background})
    return HttpResponse(plantilla.render(c))


@csrf_exempt
def usuario(request, recurso):
    regUsuarios = userLog(request)
    lusers = usuariosLateral()
    cuerpo = request.body ###
    tanda = 0
    numPag = []
    user = recurso.split('/')[-1]
    print(user)

    userReg = request.user.username
    if request.method == 'GET':
        background = css(request, user)
        # Se muestran los museos del usuario de 5 en 5
        QS = request.GET
        tanda = QS.get('numPage',default=0)
        tanda = int(tanda)
        try:
            lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)
            if len(lMuseoUser) >= tanda*5:
                numPag = range(5,len(lMuseoUser),5)
                print(len(lMuseoUser), str(tanda))
                lMuseoUser = lMuseoUser[tanda*5:(tanda+1)*5]
                tanda += 1
                print(numPag)
                #numPag.append(tanda)
        except MuseoSeleccionado.DoesNotExist:
            titulo = recurso + " no tiene museos seleccionados"
    elif request.method == 'POST':
        lMuseoUser = MuseoSeleccionado.objects.filter(usuario=recurso)
        if request.user.is_authenticated() and userReg == user:
            #user = request.user.username
            cssForm = request.POST.get('css')
            if cssForm == 'Cambiar':
                background = request.POST['fondo']
                size = request.POST['letraTam'] + 'px'
                title = request.POST['titulo']
                cssObj = Css.objects.get(usuario=user)
                if user == cssObj.usuario:
                    idcss = cssObj.id
                    cssObj = Css.objects.get(id=idcss)
                    cssObj.tamLetra = size
                    cssObj.colorFondo= background
                    cssObj.titulo=title
                    #contenido = cssObj(tamLetra=size, colorFondo=background, titulo=title)
                    cssObj.save()
                    background = css(request, user)
                    #redirect('/',user)
            else:
                if 'enviar' in request.POST:
                    #museo_id = int(request.POST.get['enviar'])
                    cuerpo = request.body.decode('utf-8')
                    museo_id = int(cuerpo.split('=')[-1])
                    ko = MuseoSeleccionado.objects.get(museo=museo_id) #get
                    ko.delete()
    plantilla = get_template("htmlCss/usuario.html")
    c = RequestContext(request,{'listaMuseos': lMuseoUser, 'login': regUsuarios,
                                'users': lusers, 'usuario':user,'tanda':tanda,
                                'listPage':numPag,'bg':background})
    return HttpResponse(plantilla.render(c))

def user_xml(request, recurso):
    user = recurso.split('/')[0]
    lMuseoUser = MuseoSeleccionado.objects.filter(usuario=user)
    hijos = serializers.serialize("xml" ,lMuseoUser)
    return HttpResponse(hijos, content_type='text/xml')
###
def barra_xml(request,formato):
    canal = recurso.split('/')[0]

def user_json(request, recurso):
    user = recurso.split('/')[0]
    lMuseoUser = MuseoSeleccionado.objects.filter(usuario=user)
    # https://docs.djangoproject.com/en/2.0/topics/serialization/
    # https://stackoverflow.com/questions/26373992/use-jsonresponse-to-serialize-a-queryset-in-django-1-7
    hijos = serializers.serialize("json", lMuseoUser)
    print(type(hijos))
    return HttpResponse(hijos, content_type="application/json")



def css(request, user):
    lusers = usuariosLateral()
    if request.method == 'GET':
        if user in lusers:
            try:
                css = Css.objects.get(usuario=user)
                #cambiaTitulo(css,user)
            except Css.DoesNotExist:
                print('no')
                css = Css(usuario=user,tamLetra='12px', colorFondo='#efefef',
                          titulo='Página de ' + user)
                css.save()
            return css
        else:
            plantilla = get_template("htmlCss/style.css")
            #c = Context({'varsCss': css })


def cambiaTitulo(css,user):
    lusers
    if not css.titulo:
        css.titulo = 'Página de ' + user
        css.save()
    css = Css.objects.get(usuario=user)
