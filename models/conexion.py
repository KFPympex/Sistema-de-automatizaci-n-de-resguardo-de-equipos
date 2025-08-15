import mysql.connector
import bcrypt

class Conexion:
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            port='tu_puerto',
            user='tu_usuario',
            password='tu contraseña',
            database='db_resguardos'
        )
        self.cursor = self.db.cursor(dictionary=True)

    def autenticar(self, nombre, contrasena):
        # 1) Intentar admin
        sql_admin = "SELECT id_admin AS id, nombre_admin AS nombre, contrasena FROM admin WHERE nombre_admin = %s"
        self.cursor.execute(sql_admin, (nombre,))
        fila = self.cursor.fetchone()
        if fila and bcrypt.checkpw(contrasena.encode(), fila['contrasena'].encode()):
            return { 'nombre': fila['nombre'], 'role': 'admin' }

        # 2) Intentar usuario normal
        sql_user = "SELECT id_usuario AS id, nombre_usuario AS nombre, contrasena FROM usuarios WHERE nombre_usuario = %s"
        self.cursor.execute(sql_user, (nombre,))
        fila = self.cursor.fetchone()
        if fila and bcrypt.checkpw(contrasena.encode(), fila['contrasena'].encode()):
            return { 'nombre': fila['nombre'], 'role': 'usuario' }

        # 3) Ninguno
        return None
    

    #Agregar Nuevo Admin
    
    def agregar_admin(self, nombre, primer_apellido_admin, segundo_apellido_admin, nombre_admin, contrasena):
        
        sql = "INSERT INTO admin (nombre, primer_apellido_admin, segundo_apellido_admin, nombre_admin, contrasena) VALUES (%s, %s, %s, %s, %s)" 

        valores = (
            nombre,
            primer_apellido_admin,
            segundo_apellido_admin,
            nombre_admin,
            contrasena.decode('utf-8') if isinstance(contrasena, bytes) else contrasena
        )
        try:
            self.cursor.execute(sql, valores)
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error al insertar usuario:", e)
            return False


    #Agregar Nuevo Usuario
    
    def agregar_usuario(self, nombre, primer_apellido_usuario, segundo_apellido_usuario, nombre_usuario, contrasena):
        
        sql = "INSERT INTO usuarios (nombre, primer_apellido_usuario, segundo_apellido_usuario, nombre_usuario, contrasena) VALUES (%s, %s, %s, %s, %s)" 

        valores = (
            nombre,
            primer_apellido_usuario,
            segundo_apellido_usuario,
            nombre_usuario,
            contrasena.decode('utf-8') if isinstance(contrasena, bytes) else contrasena
        )
        try:
            self.cursor.execute(sql, valores)
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error al insertar usuario:", e)
            return False
    

    def contar_resguardos(self):
        sql = "SELECT COUNT(*) AS total FROM resguardos"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result['total']

    ## Listar resguardos

    def listar_resguardos(self, limit=None, offset=None):
      
        sql = "SELECT r.id_resguardo, r.nombres, r.primer_apellido, r.segundo_apellido, r.numero_colaborador, r.fecha_registro, d.nombre_departamento AS departamento, p.nombre_puesto AS puesto, t.nombre_tipo AS tipo, r.marca, r.modelo, r.numero_serie, r.precio, r.nombre_entrega, er.estatus AS estatus_resguardo FROM resguardos r JOIN departamento d ON r.id_departamento = d.id_departamento JOIN puesto p ON r.id_puesto = p.id_puesto JOIN tipo t ON r.id_tipo = t.id_tipo JOIN estatus_resguardo er ON r.id_estatus_resguardo = er.id_estatus_resguardo ORDER BY r.id_resguardo"

        if limit is not None and offset is not None:
            sql += " LIMIT %s OFFSET %s"
            self.cursor.execute(sql, (limit, offset))
        else:
            self.cursor.execute(sql)
            
        return self.cursor.fetchall()

    
    
    
    def buscar_resguardo(self, texto):
        texto = f"%{texto}%"

        sql = "SELECT r.id_resguardo, r.nombres, r.primer_apellido, r.segundo_apellido, r.numero_colaborador, r.fecha_registro, d.nombre_departamento AS departamento, p.nombre_puesto AS puesto, t.nombre_tipo AS tipo, r.marca, r.modelo, r.numero_serie, r.precio, r.nombre_entrega, er.estatus AS estatus_resguardo FROM resguardos r JOIN departamento d ON r.id_departamento = d.id_departamento JOIN puesto p ON r.id_puesto = p.id_puesto JOIN tipo t ON r.id_tipo = t.id_tipo JOIN estatus_resguardo er ON r.id_estatus_resguardo = er.id_estatus_resguardo WHERE LOWER(CONCAT(r.nombres, ' ', r.primer_apellido, ' ', r.segundo_apellido)) LIKE LOWER(%s) OR r.nombres LIKE %s OR r.primer_apellido LIKE %s OR r.segundo_apellido LIKE %s OR r.numero_colaborador LIKE %s OR d.nombre_departamento LIKE %s OR p.nombre_puesto LIKE %s OR t.nombre_tipo LIKE %s OR r.marca LIKE %s OR r.modelo LIKE %s OR r.numero_serie LIKE %s OR r.nombre_entrega LIKE %s ORDER BY r.id_resguardo"

        valores = (texto, texto, texto, texto, texto, texto, texto, texto, texto, texto, texto, texto)
        self.cursor.execute(sql, valores)
        return self.cursor.fetchall()
    
    
    ## Agregar nuevo resguardo
    
    def listar_departamentos(self):
        self.cursor.execute("SELECT id_departamento, nombre_departamento FROM departamento")
        return self.cursor.fetchall()
    
    def listar_puestos(self):
        self.cursor.execute("SELECT id_puesto, nombre_puesto FROM puesto")
        return self.cursor.fetchall()
    
    def listar_tipos(self):
        self.cursor.execute("SELECT id_tipo, nombre_tipo FROM tipo")
        return self.cursor.fetchall()
    
    def listar_estatus_resguardos(self):
        self.cursor.execute("SELECT id_estatus_resguardo, estatus FROM estatus_resguardo")
        return self.cursor.fetchall()
    
    def agregar_resguardo(self, nombres, primer_apellido, segundo_apellido, numero_colaborador, id_departamento, id_puesto, id_tipo, marca, modelo, numero_serie, precio, nombre_entrega, id_estatus_resguardo):

        sql = "INSERT INTO resguardos (nombres, primer_apellido, segundo_apellido, numero_colaborador, id_departamento, id_puesto, id_tipo, marca, modelo, numero_serie, precio, nombre_entrega, id_estatus_resguardo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        valores = (
            nombres, 
            primer_apellido,
            segundo_apellido,
            numero_colaborador,
            id_departamento,
            id_puesto,
            id_tipo,
            marca,
            modelo,
            numero_serie,
            precio,
            nombre_entrega, 
            id_estatus_resguardo
        )
        try:

            self.cursor.execute(sql, valores)
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error al insertar resguardo:", e)
            return False
        

    ## Editar resguardo por ID

    def editar_resguardo(self, id_resguardo, nombres, primer_apellido, segundo_apellido, numero_colaborador, id_departamento, id_puesto, id_tipo, marca, modelo, numero_serie, precio, nombre_entrega, id_estatus_resguardo):

        sql = "UPDATE resguardos SET nombres = %s, primer_apellido = %s, segundo_apellido = %s, numero_colaborador = %s, id_departamento = %s, id_puesto = %s, id_tipo = %s, marca = %s, modelo = %s, numero_serie = %s, precio = %s, nombre_entrega = %s, id_estatus_resguardo = %s WHERE id_resguardo = %s"
        
        valores = (
            nombres,
            primer_apellido,
            segundo_apellido,
            numero_colaborador,
            id_departamento,
            id_puesto,
            id_tipo,
            marca,
            modelo,
            numero_serie,
            precio,
            nombre_entrega,
            id_estatus_resguardo,
            id_resguardo
        )
        
        try:
            self.cursor.execute(sql, valores)
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error al actualizar resguardo:", e)
            return False


    ## Eliminar resguardo por ID

    def borrar_resguardo(self, id_resguardo):
        sql = "DELETE FROM resguardos WHERE id_resguardo = %s"
        try:
            self.cursor.execute(sql, (id_resguardo,))
            self.db.commit()
            return True
        except mysql.connector.Error as e:
            print("Error al borrar resguardo:", e)
            return False


    ## Ver detalle del PDF del resguardo por ID 

    def detalle_pdf_resguardo(self, id_resguardo):
        sql = "SELECT r.id_resguardo, r.nombres, r.primer_apellido, r.segundo_apellido, r.numero_colaborador, r.fecha_registro, r.id_departamento, d.nombre_departamento AS departamento, r.id_puesto, p.nombre_puesto AS puesto, r.id_tipo, t.nombre_tipo AS tipo, r.marca, r.modelo, r.numero_serie, r.precio, r.nombre_entrega, r.id_estatus_resguardo, er.estatus AS estatus_resguardo FROM resguardos r JOIN departamento d ON r.id_departamento = d.id_departamento JOIN puesto p ON r.id_puesto = p.id_puesto JOIN tipo t ON r.id_tipo = t.id_tipo JOIN estatus_resguardo er ON r.id_estatus_resguardo = er.id_estatus_resguardo WHERE r.id_resguardo = %s"

        self.cursor.execute(sql, (id_resguardo,))
        return self.cursor.fetchone()
    

    ## Generar PDF de resguardo por ID

    def generar_pdf_resguardo(self, id_resguardo):
        sql = """
        SELECT
          r.id_resguardo, r.nombres, r.primer_apellido, r.segundo_apellido, r.numero_colaborador,
          r.fecha_registro, d.nombre_departamento AS departamento,
          p.nombre_puesto AS puesto, t.nombre_tipo AS tipo,
          r.marca, r.modelo, r.numero_serie, r.precio, r.nombre_entrega,
          er.estatus AS estatus_resguardo
        FROM resguardos r
        JOIN departamento d  ON r.id_departamento = d.id_departamento
        JOIN puesto p        ON r.id_puesto      = p.id_puesto
        JOIN tipo t          ON r.id_tipo        = t.id_tipo
        JOIN estatus_resguardo er ON r.id_estatus_resguardo = er.id_estatus_resguardo
        WHERE r.id_resguardo = %s
        """
        self.cursor.execute(sql, (id_resguardo,))
        return self.cursor.fetchone()