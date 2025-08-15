import web

class Logout:
    def GET(self):
        sess = web.config.session
        sess.kill()  # Termina la sesión actual
        raise web.seeother('/')