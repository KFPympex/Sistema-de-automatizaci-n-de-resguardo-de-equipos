import web
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion 

render = web.template.render('views/resguardos/', base='master')

class DetallePDFResguardo:
    def GET(self, id_resguardo):
        seguridad()
        model = Conexion()
        r = model.detalle_pdf_resguardo(int(id_resguardo))
        if not r:
            return web.notfound("Resguardo no encontrado")
        return render.detalle_pdf_resguardo(r)
    

