import web, bcrypt
from controllers.utils.seguridad import seguridad
from models.conexion import Conexion

render = web.template.render('views/admin/')

class AgregarUsuario:
    def GET(self):
        seguridad('admin')
        return render.agregar_usuario(error=None)

    def POST(self):
        seguridad('admin')
        datos = web.input()
        nombre = datos.nombre
        primer_apellido_usuario = datos.primer_apellido_usuario
        segundo_apellido_usuario = datos.segundo_apellido_usuario
        nombre_usuario   = datos.nombre_usuario
        contrasena  = datos.contrasena

        # Hasheamos la contraseña
        contr_hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        modelo = Conexion()
        ok = modelo.agregar_usuario(nombre, primer_apellido_usuario, segundo_apellido_usuario, nombre_usuario, contr_hashed)
        if not ok:
            # si el modelo devolvió False, mostramos mensaje
            return render.agregar_usuario(error="No se pudo agregar el nuevo usuario, el nombre de usuario ya existe.")
        # Si todo va bien, redirigimos al admin
        raise web.seeother('/bienvenida_admin')
