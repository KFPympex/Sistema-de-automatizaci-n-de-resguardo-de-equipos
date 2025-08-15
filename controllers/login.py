import web
from models.conexion import Conexion

render = web.template.render('views/')


class Login:
    def GET(self):
        sess = web.config.session
        # Si ya está autenticado, mandar al dashboard según rol
        if sess.logged_in:
            return self._redir_por_rol(sess.role)
        return render.login()

    def POST(self):
        form    = web.input()
        nombre  = form.nombre_usuario
        passwd  = form.contrasena

        modelo  = Conexion()
        userobj = modelo.autenticar(nombre, passwd)

        if not userobj:
            return render.login(error="Credenciales incorrectas.")

        #  Guardamos en sesión
        sess = web.config.session
        sess.logged_in = True
        sess.nombre    = userobj['nombre']
        sess.role      = userobj['role']

        return self._redir_por_rol(sess.role)

    def _redir_por_rol(self, role):
        if role == 'admin':
            raise web.seeother('/bienvenida_admin')
        else:
            raise web.seeother('/bienvenida_usuario')
