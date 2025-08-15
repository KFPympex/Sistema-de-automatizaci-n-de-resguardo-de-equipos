import web
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion

render = web.template.render('views/resguardos/', base='master')

class BuscarResguardo:
    def POST(self):
        seguridad()
        datos = web.input(busqueda='')
        termino = datos.busqueda.strip()
        # redirige a ListarResguardos manejando parámetros
        url = '/listar_resguardos?page=1'
        if termino:
            url += '&buscar=' + web.urlquote(termino)
        raise web.seeother(url)