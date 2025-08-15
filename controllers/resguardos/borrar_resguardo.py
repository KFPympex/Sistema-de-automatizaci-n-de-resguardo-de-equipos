import web
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion

class BorrarResguardo:
    def POST(self, id_resguardo):
        seguridad()
        model = Conexion()
        model.borrar_resguardo(int(id_resguardo))
        raise web.seeother('/listar_resguardos')
    
