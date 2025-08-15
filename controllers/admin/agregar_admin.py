import web, bcrypt
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion

render = web.template.render('views/admin/')

class AgregarAdmin:
    def GET(self):
        seguridad('admin')
        return render.agregar_admin(error=None)

    def POST(self):
        seguridad('admin')
        datos = web.input()
        nombre = datos.nombre
        primer_apellido_admin = datos.primer_apellido_admin
        segundo_apellido_admin = datos.segundo_apellido_admin
        nombre_admin   = datos.nombre_admin
        contrasena  = datos.contrasena

        # Hasheamos la contraseña
        contr_hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        modelo = Conexion()
        ok = modelo.agregar_admin(nombre, primer_apellido_admin, segundo_apellido_admin, nombre_admin, contr_hashed)
        if not ok:
            # si el modelo devolvió False, mostramos mensaje
            return render.agregar_admin(error="No se pudo agregar el nuevo administrador, el nombre de administrador ya existe.")
        # Si todo va bien, redirigimos al admin
        
        raise web.seeother('/bienvenida_admin')
