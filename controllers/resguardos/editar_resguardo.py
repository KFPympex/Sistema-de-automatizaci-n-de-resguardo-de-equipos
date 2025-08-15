import web
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion 

render = web.template.render('views/resguardos/', base='master')

class EditarResguardo:
    def GET(self, id_resguardo):
        seguridad()
        model = Conexion()
        r = model.detalle_pdf_resguardo(int(id_resguardo))
        if not r:
            return "Resguardo no encontrado."
        
        departamento = model.listar_departamentos()
        puesto = model.listar_puestos()
        tipo = model.listar_tipos()
        estatus_resguardo = model.listar_estatus_resguardos()
        
        return render.editar_resguardo(r, departamento, puesto, tipo, estatus_resguardo)
    
    def POST(self, id_resguardo):
        seguridad()
        i = web.input(
            nombres="",
            primer_apellido="",
            segundo_apellido="",
            numero_colaborador="",
            id_departamento="",
            id_puesto="",
            id_tipo="",
            marca="",
            modelo="",
            numero_serie="",
            precio="",
            nombre_entrega="",
            id_estatus_resguardo=""
        )

        model = Conexion()
        model.editar_resguardo(
            int(id_resguardo),
            i.nombres,
            i.primer_apellido,
            i.segundo_apellido,
            i.numero_colaborador,
            int(i.id_departamento),
            int(i.id_puesto),
            int(i.id_tipo),
            i.marca,
            i.modelo,
            i.numero_serie,
            float(i.precio),
            i.nombre_entrega,
            int(i.id_estatus_resguardo)       
        )
        if not i:
            return "Error al actualizar el resguardo."
        raise web.seeother('/listar_resguardos')

    

