@csrf_exempt
def home(request): #pagina principal
    if request.method == "GET": #Ordenamos por aparcamientos mas comentados
        titulo = texto("comentados")
        boton = form("accesible","","")
        parkings = Aparcamientos.objects.all() #con all no tenemos excepcion!
        
        if len(parkings) == 0):
          noDataHtml()
        else:
          titulo = texto("comentados")
          boton = form("accesible","","")
          parkingsOrdenados = parkings.order_by('-nComen')
          content = listado(parkingsOrdenados, request, 0, request.user) #listado de parkings

    elif request.method == 'POST': #aqui tratamos solo el post del boton accesibles
        valor = request.POST ['boton']

        if (valor == "ACCESIBLES"): #Aparcamientos accesibles
            titulo = texto("accesible")
            boton = form("accesible2","","") #pasamos a mostrar boton de "ir a mas comentados"
            parkings = Aparcamientos.objects.filter(accesibilidad=1)
            aparcamientos = parkings.order_by('-nComen')
            content = listado(aparcamientos, request, 0, request.user) #listado de parkings accesibles

        else: #Aparcamientos mas comentados
            titulo = texto("comentados")
            boton = form("accesible","","") #pasamos a mostrar de nuevo boton de "ir a accesibles"
            parkings = Aparcamientos.objects.all()
            aparcamientos = parkings.order_by('-nComen')
            content = listado(aparcamientos,request, 0, request.user) #listado de parkings


    #Paginas Personales
    datos = paginasUsers()

    #Ahora renderizamos
    log = logInOut(request)
    links = linksHome() #links todos, about
    template = get_template("home.html")
    c = Context ({'log': log,
                  'links': links,
                  'boton': boton,
                  'titulo': titulo,
                  'content': content,
                  'datos': datos})
    return HttpResponse(template.render(c))




##CAMBIAR EN URL.PY --> /getData, views.getDatos
def noDataHtml():
   boton = form ("datos", "", "")  -->  "<form action='/getData' method='GET'><button type='submit' name='Recargar'>Obtener Datos</button></form>"
           content = "No hay aparcamientos. ¿Cargar? --> " + botonRecarga
           plantilla =  get_template('home.html')
           log = logInOut(request)
           links = linksHome() #links todos, about
           template = get_template("home.html")
           c = Context ({'log': log,
                      'links': links,
                      'content': content})
            return HttpResponse(plantilla.render(c))


#INCLUIR IMPORTS AL PRINCIPIO DEL FICHERO!!!!!
def parseAdd(request): #Parseamos XML y creamos objetos Aparcamiento
     xmlFile = urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
     arbol = ET.parse(xmlFile)
     raiz = arbol.getroot()

            for elem in arbol.iter():
                if "ID-ENTIDAD" in elem.attrib.values():   # Es un diccionario
                    nuevoAparcamiento = Aparcamiento(idEntidad=elem.text)
                elif "NOMBRE" in elem.attrib.values():
                    nuevoAparcamiento.nombre = elem.text
                elif "DESCRIPCION" in elem.attrib.values():
                    nuevoAparcamiento.descripcion = elem.text
                elif "ACCESIBILIDAD" in elem.attrib.values():
                    nuevoAparcamiento.accesibilidad = elem.text
                elif "CONTENT-URL" in elem.attrib.values():
                    nuevoAparcamiento.contentUrl = elem.text
                elif "NOMBRE-VIA" in elem.attrib.values():
                    nuevoAparcamiento.nombreVia = elem.text
                elif "CLASE-VIAL" in elem.attrib.values():
                    nuevoAparcamiento.claseVial = elem.text
                elif "TIPO-NUM" in elem.attrib.values():
                    nuevoAparcamiento.tipoNum = elem.text
                elif "NUM" in elem.attrib.values():
                    nuevoAparcamiento.num = elem.text
                elif "ORIENTACION" in elem.attrib.values():
                    nuevoAparcamiento.orientacion = elem.text
                elif "LOCALIDAD" in elem.attrib.values():
                    nuevoAparcamiento.localidad = elem.text
                elif "PROVINCIA" in elem.attrib.values():
                    nuevoAparcamiento.provincia = elem.text
                elif "CODIGO-POSTAL" in elem.attrib.values():
                    nuevoAparcamiento.codigoPostal = elem.text
                elif "BARRIO" in elem.attrib.values():
                    nuevoAparcamiento.barrio = elem.text
                elif "DISTRITO" in elem.attrib.values():
                    nuevoAparcamiento.distrito = elem.text
                elif "COORDENADA-X" in elem.attrib.values():
                    nuevoAparcamiento.coordenadaX = elem.text
                elif "COORDENADA-Y" in elem.attrib.values():
                    nuevoAparcamiento.coordenadaY = elem.text
                elif "LATITUD" in elem.attrib.values():
                    nuevoAparcamiento.latitud = elem.text
                elif "LONGITUD" in elem.attrib.values():
                    nuevoAparcamiento.longitud = elem.text
                elif "TELEFONO" in elem.attrib.values():
                    nuevoAparcamiento.telefono = elem.text
                elif "EMAIL" in elem.attrib.values():
                    nuevoAparcamiento.email = elem.text
                elif "TIPO" in elem.attrib.values():
                    nuevoAparcamiento.save()
                else:
                    pass

















@csrf_exempt
def loginPS(request):
    nick = request.POST['name']
    password = request.POST['pass']
    user = authenticate(username=nick, password=password)

    if user is not None: #correcto, redireccionamos
        login(request, user)
        return redirect(home)

    else: #Nick o pass incorrectos
        #CAMBIOOOS
        log = form("logError", "", "") #formulario de error de sign in
        links = linksHome() #links Inicio, todos, about
        content = "Usuario o contraseña incorrectos. Prueba de nuevo"

        template = get_template("home.html") #cambia el content de home.html
        c = Context ({'log': log,
                      'links': links,
                      'content': content})
        return HttpResponse(template.render(c))
        
        
        
##En FORM HACER UN NUEVO IF        
if tipo == "logError": #Nuevo form para login, dado el error de autentificacion
     log = "<form class='.t-left' action='/' method='POST'>" \
         + "<label><strong>Wrong Nick or Pass. Try again</strong><br></label>" \
         + "NICK:  <input type='text' name='name'><br>" \
         + "PASS: <input type='password' name='pass'><br> "\
         + "<input type='submit' value='Submit'></form>"
    
    return tipo
