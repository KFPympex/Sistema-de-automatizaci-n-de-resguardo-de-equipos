import web

from web.session import Session 

from controllers.login import Login as Login
from controllers.logout import Logout as Logout
from controllers.admin.bienvenida_admin import BienvenidaAdmin as BienvenidaAdmin
from controllers.usuarios.bienvenida_usuario import BienvenidaUsuario as BienvenidaUsuario
from controllers.admin.agregar_admin import AgregarAdmin as AgregarAdmin
from controllers.admin.agregar_usuario import AgregarUsuario as AgregarUsuario
from controllers.resguardos.listar_resguardos import ListarResguardos as ListarResguardos
from controllers.resguardos.buscar_resguardo import BuscarResguardo as BuscarResguardo
from controllers.resguardos.agregar_resguardo import AgregarResguardo as AgregarResguardo
from controllers.resguardos.detalle_pdf_resguardo import DetallePDFResguardo as DetallePDFResguardo
from controllers.resguardos.editar_resguardo import EditarResguardo as EditarResguardo
from controllers.resguardos.borrar_resguardo import BorrarResguardo as BorrarResguardo
from controllers.resguardos.generar_pdf_resguardo import GenerarPDFResguardo as GenerarPDFResguardo

urls = (
    '/', 'Login',
    '/logout', 'Logout',
    '/bienvenida_admin', 'BienvenidaAdmin',
    '/bienvenida_usuario', 'BienvenidaUsuario',
    '/agregar_admin', 'AgregarAdmin',
    '/agregar_usuario', 'AgregarUsuario',
    '/listar_resguardos', 'ListarResguardos',
    '/buscar_resguardo', 'BuscarResguardo',
    '/agregar_resguardo', 'AgregarResguardo',
    '/detalle_pdf_resguardo/(\d+)', 'DetallePDFResguardo',
    '/editar_resguardo/(\d+)', 'EditarResguardo',
    '/borrar_resguardo/(\d+)', 'BorrarResguardo',
    '/generar_pdf_resguardo/(\d+)', 'GenerarPDFResguardo',

)

app = web.application(urls, globals())

store = web.session.DiskStore('sessions')
session = Session (app, store, initializer = {'logged_in': False, 'usuario': None, 'role': None })
web.config.session = session

if __name__ == "__main__":
       app.run()
       