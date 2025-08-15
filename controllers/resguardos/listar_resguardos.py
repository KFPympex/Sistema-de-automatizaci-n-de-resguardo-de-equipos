import web
import math
from controllers.utils.seguridad import seguridad 
from models.conexion import Conexion 
   
render = web.template.render('views/resguardos/', base='master')

PER_PAGE = 5  # registros por página

class ListarResguardos:
    def GET(self):
        seguridad()
        datos = web.input(page='1', buscar='')  # leer page y buscar si viene
        page = int(datos.page) if datos.page.isdigit() and int(datos.page) > 0 else 1
        texto = datos.buscar.strip()

        conexion = Conexion()
        # traer todos o buscar
        if texto:
            todos = conexion.buscar_resguardo(texto)
        else:
            todos = conexion.listar_resguardos()

        total = len(todos)
        total_pages = max(1, math.ceil(total / PER_PAGE))
        # ajustar page dentro de rango
        if page > total_pages:
            page = total_pages

        start = (page - 1) * PER_PAGE
        end = start + PER_PAGE
        resguardos = todos[start:end]

        return render.listar_resguardos(
            resguardos=resguardos,
            page=page,
            total_pages=total_pages,
            buscar=texto
        )

    def POST(self):
        # redirigir POST a GET para mantener la paginación en la búsqueda
        seguridad()
        datos = web.input(buscar='')
        texto = datos.buscar.strip()
        # construimos URL con parámetros
        url = '/listar_resguardos?page=1'
        if texto:
            url += '&buscar=' + web.urlquote(texto)
        raise web.seeother(url)