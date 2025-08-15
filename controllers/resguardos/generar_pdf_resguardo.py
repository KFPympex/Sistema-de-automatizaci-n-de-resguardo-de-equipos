import web
import locale
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from models.conexion import Conexion

class GenerarPDFResguardo:
    def GET(self, id_resguardo):

        datos = Conexion().generar_pdf_resguardo(int(id_resguardo))
        if not datos:
            return web.notfound("Resguardo no encontrado")

        try:
            locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        fecha_orig = datos['fecha_registro']

        if isinstance(fecha_orig, str):
            fecha_dt = datetime.strptime(fecha_orig, '%Y-%m-%d %H:%M:%S')
        elif isinstance(fecha_orig, datetime):
            fecha_dt = fecha_orig
        else:
            fecha_dt = datetime.strptime(str(fecha_orig), '%Y-%m-%d %H:%M:%S')

        fecha_formato = f"{fecha_dt.day} {fecha_dt.strftime('%B')} de {fecha_dt.year}"

        reader = PdfReader("static/pdf/resguardo_formato.pdf")
        writer = PdfWriter()
        page = reader.pages[0]

        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        campos = [
        #     X    Y
            (426, 693, "", fecha_formato),  
            (170, 620, "", datos['tipo']),
            (205, 620, "", f"{datos['marca']} {datos['modelo']}"),
            (173, 605, "S/N:", datos['numero_serie']),
            (455, 595, "", f"${datos['precio']}"),
        ]
    
        # Tamaño de fuente para los campos
        can.setFont("Helvetica", 10)
        for x, y, etiqueta, campo in campos:
            can.drawString(x, y, f"{etiqueta} {campo}")
            

        # Nombre de fuente y tamaño del nombre completo y quien entrega
        font_name, font_size = "Helvetica", 10

        # Nombre completo, con caja X=[102, 270], Y=255
        x0, x1, y_nombres = 102, 270, 255
        texto_nombres = f"{datos['nombres']} {datos['primer_apellido']} {datos['segundo_apellido']}"
        can.setFont(font_name, font_size)
        w = can.stringWidth(texto_nombres, font_name, font_size)
        x_nombres = x0 + max(0, (x1 - x0 - w) / 2)
        can.drawString(x_nombres, y_nombres, texto_nombres)

        # Nombre de quien entrega, con caja X=[338, 515], Y=260
        x0, x1, y_entrega = 338, 515, 260
        texto_entrega = datos['nombre_entrega']
        w2 = can.stringWidth(texto_entrega, font_name, font_size)
        x_entrega = x0 + max(0, (x1 - x0 - w2) / 2)
        can.drawString(x_entrega, y_entrega, texto_entrega)

        # Departamento, con caja X=[102, 270], Y=242    
        x0, x1, y = 102, 270, 242   
        font_name = "Helvetica"
        font_size = 8
        texto = datos['departamento']

        can.setFont(font_name, font_size)
        text_width = can.stringWidth(texto, font_name, font_size)
        width_box = x1 - x0

        # Centro horizontal
        x_text = x0 + max(0, (width_box - text_width) / 2)

        can.drawString(x_text, y, texto)
        
        can.save()
        packet.seek(0)
        overlay = PdfReader(packet).pages[0]
        page.merge_page(overlay)

        writer.add_page(page)
        for p in reader.pages[1:]:
            writer.add_page(p)

        pdf_bytes = BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)

        web.header("Content-Type", "application/pdf")
        web.header(
            "Content-Disposition",
            f"inline; filename=\"resguardo-{datos['id_resguardo']}-"
            f"{datos['nombres']}-{datos['primer_apellido']}-{datos['segundo_apellido']}.pdf\""
        )
        return pdf_bytes.read()
