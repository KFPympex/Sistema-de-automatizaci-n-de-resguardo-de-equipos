import web
from controllers.utils.seguridad import seguridad 


render = web.template.render('views/usuario/')

class BienvenidaUsuario:
    def GET(self):
        seguridad()
        sess = web.config.session
        if not sess.logged_in or sess.role != 'usuario':
            raise web.seeother('/')
        return render.bienvenida_usuario(usuario=sess.nombre)