import web

render = web.template.render('views/')

def seguridad(role=None):
    sess = web.config.session
    if not sess.logged_in:
        raise web.seeother('/')
    if role and sess.role !=role:
        raise web.seeother('/')