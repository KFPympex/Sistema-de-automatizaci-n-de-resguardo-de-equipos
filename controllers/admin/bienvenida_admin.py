import web
from controllers.utils.seguridad import seguridad 


render = web.template.render('views/admin/')

class BienvenidaAdmin :
    def GET(self):
        seguridad()
        sess = web.config.session
        if not sess.logged_in or sess.role != 'admin':
            raise web.seeother('/')
        return render.bienvenida_admin(usuario=sess.nombre)

