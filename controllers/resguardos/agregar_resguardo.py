import web
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion 
   
render = web.template.render('views/resguardos/', base='master')

class AgregarResguardo:
    def GET(self):
        seguridad()
        model = Conexion()
        departamento = model.listar_departamentos()
        puesto = model.listar_puestos()
        tipo = model.listar_tipos()
        estatus_resguardo = model.listar_estatus_resguardos()
        return render.agregar_resguardo(departamento, puesto, tipo, estatus_resguardo)
    
    def POST(self):
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
        model.agregar_resguardo(
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
            i.precio,
            i.nombre_entrega,
            int(i.id_estatus_resguardo)       
        )

        raise web.seeother('/listar_resguardos')